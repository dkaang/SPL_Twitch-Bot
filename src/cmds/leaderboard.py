from .. import db

def leaderboard(bot, user, *args):
    users = db.records(f"SELECT UserID, UserName, Coins FROM users") # [('407112021', 'Tiqan_', 13), ('125313114', 'yung_yoom', 13)]
    
    sorted_users = sorted(users, key=lambda x: x[2], reverse=True)
    sorted_users = sorted_users[:5]
    leaderboard_text = "🏆 Leaderboard:"
    for i, user in enumerate(sorted_users, 1):
        leaderboard_text += f" -- {i}. {user[1]}: {user[2]} coins"
    bot.send_message(leaderboard_text)
    
    
    