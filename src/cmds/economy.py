from .. import db

def coins(bot, user, *args):
    coins = db.field("SELECT Coins FROM users WHERE UserID = ?", user["id"])

    bot.send_message(f"{user['name']}, du hast {coins:,} Coins.")

