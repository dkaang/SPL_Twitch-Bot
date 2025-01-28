from time import time

from . import misc

PREFIX = "!" # e,g, "!hello"

class Cmd(object):
    def __init__(self, callables, func, cooldown = 0):
        self.callables: list = callables # list of callables you can use
        self.func = func
        self.cooldown: int = cooldown # cooldown period in seconds
        self.next_use = time() # gets checked against the cooldown


# cmds = {
#     "hello": misc.hello, # cmd | func
# }

cmds = [
    Cmd(["hello", "hi", "hey"], misc.hello, cooldown = 15)
]

def process(bot, user, message):
    if message.startswith(PREFIX):
        cmd = message.split(" ")[0][len(PREFIX):] # "!hello" -> "hello"
        args = message.split(" ")[1:]
        perform(bot, user, cmd, *args)


def perform(bot, user, call, *args): # call = cmd
    if call in ("help", "commands", "cmds"):
        misc.help(bot, PREFIX, cmds)
        
    else:
        for cmd in cmds:
            if call in cmd.callables:
                if time() > cmd.next_use:
                    cmd.func(bot, user, *args)
                    cmd.next_use = time() + cmd.cooldown # present time + cooldown (15 seconds)

                else:
                    bot.send_message(f"{user['name']}, {call} is still on cooldown. \nTry again in {cmd.next_use - time():,.0f} seconds.")
                
                return
        bot.send_message(f"{user['name']}, \"{call}\" isn't a registered command.") # if cmd is run, it will never get to this point


# def perform(bot, user, cmd, *args):
#     for name, func in cmds.items():
#         if cmd == name:
#             func(bot, user, *args)
#             return
        
#     if cmd == "help":
#         misc.help(bot, PREFIX, cmds)

#     else:
#         bot.send_message(f"{user['name']}, \"{cmd}\" isn't a registered command.")

