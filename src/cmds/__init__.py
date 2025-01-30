from time import time

from . import misc, economy, games, voteSystem, leaderboard

from .. import db

PREFIX = "!" # e,g, "!hello"

class Cmd(object):
    def __init__(self, callables, func, cooldown_key, cooldown = 0):
        self.callables: list = callables # list of callables you can use
        self.func = func
        self.cooldown: int = cooldown # cooldown period in seconds
        self.cooldown_key: str = cooldown_key
        self.cooldown_message: str = "{username}, {call} ist noch auf cooldown. \nVersuch's in {time} Seconds erneut."

#         self.cooldown_message: str = f"{user['name']}, {call} is still on cooldown. \nTry again in {cmd.next_use - time():,.0f} seconds."

# cmds = {
#     "hello": misc.hello, # cmd | func
# }

cmds = [
    #   economy
    Cmd(["coins", "money", "balance"], economy.coins, cooldown=30, cooldown_key = "LastCoins"),

    #   games
    Cmd(["coinflip", "flip"], games.coinflip, cooldown = 60, cooldown_key = "LastCoinFlip"), 
    # Cmd(["rockpaperscissors", "rps"], games.rockpaperscissors, cooldown = 300)

    #   votes
    Cmd(["vote_start"], voteSystem.vote_start, cooldown=0, cooldown_key="LastVoteStart"),
    Cmd(["vote_end"], voteSystem.vote_end, cooldown=0, cooldown_key="LastVoteStart"),
    Cmd(["vote"], voteSystem.vote, cooldown=0, cooldown_key="LastVoteStart"),
    
    #   leaderboard
    Cmd(["leaderboard", "ld"], leaderboard.leaderboard, cooldown=150, cooldown_key="LastLeaderboard")
]

def process(bot, user, message):
    if message.startswith(PREFIX):
        cmd = message.split(" ")[0][len(PREFIX):] # "!hello" -> "hello"
        args = message.split(" ")[1:]
        perform(bot, user, cmd, *args)


def perform(bot, user, call, *args): # call = cmd
    if call in ("help", "commands", "cmds"):
        misc.help(bot, PREFIX, cmds)
        return
        
    for cmd in cmds:
        if call in cmd.callables: 
            try:
                with open("messages.txt", "r+") as f:
                    count = int(f.read() or "0")
                    count += 1
                    f.seek(0)
                    f.write(str(count))
            except FileNotFoundError:
                with open("messages.txt", "w") as f:
                    f.write("1")
            last_cooldown = db.field(f"SELECT {cmd.cooldown_key} FROM cooldowns WHERE UserID = ?", user["id"])
            if last_cooldown is not None:
                if (time() - last_cooldown) < cmd.cooldown:
                    bot.send_message(cmd.cooldown_message.format(username=user["name"], call=call, time="{:.0f}".format(cmd.cooldown - (time() - last_cooldown))))
                    return
            
            # db entry for cooldowns
            sql = f"INSERT INTO cooldowns (UserID, {cmd.cooldown_key}) VALUES (?, ?) ON CONFLICT (UserID) DO UPDATE SET {cmd.cooldown_key} = ?"
            db.execute(sql, user["id"], time(), time())
            cmd.func(bot, user, *args)
            return
            
    bot.send_message(f"{user['name']}, \"{call}\" ist kein registrierter Command.")

