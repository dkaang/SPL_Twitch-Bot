from collections import defaultdict
from re import search
from random import randint
from datetime import datetime, timedelta

from . import db

welcomed = []
messages = defaultdict(int)


def process(bot, user, message):
    update_records(bot, user)

    if user["id"] not in welcomed:
        welcome(bot, user)

    elif "bye" in message.lower():
        goodbye(bot, user)

    # check_activity(bot, user) # lowkey nervig und useless, aber fine zum testen | SPÄTER AUSKOMMENTIEREN !!!


def update_records(bot, user):
    db.execute("INSERT OR IGNORE INTO users (UserID, UserName) VALUES (?, ?)", 
               user["id"], user["name"]) # insert user into database if not already there

    db.execute("UPDATE users SET MessagesSent = MessagesSent + 1 WHERE UserID = ?", 
               user["id"]) # increment the number of messages sent by the user
    
    stamp = db.field("SELECT CoinLock FROM users WHERE UserID = ?", user["id"])

    if datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S") < datetime.utcnow(): # datetime.utcnow()
        coinLock = (datetime.utcnow() + timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M:%S") # return an object one minute in the future | seconds=60
        
        db.execute("UPDATE users SET Coins = Coins + ?, CoinLock = ? WHERE UserID = ?", 
                   randint(5,10), coinLock, user["id"])

    

def welcome(bot, user):
    bot.send_message(f"Welcome to the Stream {user['name']}! :)")
    welcomed.append(user["id"])

def goodbye(bot, user):
    bot.send_message(f"Goodbye {user['name']}! See you soon! :)")
    welcomed.remove(user["id"]) # if not commeted out, the bot will welcome the user again, the next time they send a message (after saying "bye")


def check_activity(bot, user):
    messages[user["id"]] += 1 # only works, because it is a defaultdict

    if (count := messages[user["id"]]) % 3 == 0: # increase the number 3 to about 25 - for now its 3 for testing purposes 
        bot.send_message(f"Thanks for being active in chat {user['name']} - you've sent {count:,} messages! Keep it up!") # ":," = thounsands separator


""" 
Duelling System functionality:

Message from yung_yoom: '!duel <enemy>'
Message from yung_yoom: '!duel accept <player1>'

"""

