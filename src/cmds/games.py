from random import choice, randint
from time import time

from .. import db

def coinflip(bot, user, side=None, bet=5, *args): # *args, to eat up and prevent user from inputting more than 1 argument 
    bet = int(bet)
    
    if side is None:
        bot.send_message("You need to guess which side the coin will land on!")

    elif (side := side.lower()) not in (opt := ("heads", "tails", "head", "tail", "h", "t")):
        bot.send_message("Enter one of the following as the side: " + "/".join(opt))

    else:
        

        user_coins = db.field("SELECT Coins FROM users WHERE UserID = ?", user["id"])

        if user_coins < bet:
            bot.send_message(f"{user['name']}, you don't have enough coins to make that bet.")
            return

        result = choice(("heads", "tails"))

        if side[0] == result[0]: # compare first letter of side and first letter of result -> side: "h" | result: "heads" => correct
            db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?", bet, user["id"])
            bot.send_message(f"The coin landed on {result}! You won. :D")

        else:
            db.execute("UPDATE users SET Coins = Coins - ? WHERE UserID = ?", bet, user["id"])
            bot.send_message(f"Too bad - it landed on {result}. You lost your bet. :(")
        
