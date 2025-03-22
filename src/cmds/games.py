from random import choice, randint
from time import time

from .. import db

def coinflip(bot, user, side=None, bet=5, *args): # *args, to eat up and prevent user from inputting more than 1 argument 
    try:
        bet = int(bet)
    except:
        return
    bet = int(bet)
    
    if bet <= 0:
        return

    if side is None:
        bot.send_message("Errate, auf welcher Seite die Münze landen wird! Benutz: !coinflip <kopf/zahl> <bet>")

    elif (side := side.lower()) not in (opt := ("kopf", "zahl", "k", "z")):
        bot.send_message("Such dir eine von den folgenden Seiten aus: " + " / ".join(opt))

    else:
        user_coins = db.field("SELECT Coins FROM users WHERE UserID = ?", user["id"])

        if user_coins < bet:
            bot.send_message(f"{user['name']}, du hast nicht genügend Coins, um diese Wette abzugeben.")
            return

        result = choice(("kopf", "zahl"))

        if side[0] == result[0]: # compare first letter of side and first letter of result -> side: "h" | result: "heads" => correct
            db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?", bet, user["id"])
            bot.send_message(f"Die Münze ist auf {result.title()} gelandet! Du hast gewonnen! :D")

        else:
            db.execute("UPDATE users SET Coins = Coins - ? WHERE UserID = ?", bet, user["id"])
            bot.send_message(f"Schade - die Münze ist auf {result.title()} gelandet. Du hast verloren. :(")
