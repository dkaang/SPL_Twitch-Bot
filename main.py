"""
    COPYRIGHT INFORMATION
    ---------------------

Some code in this file is licensed under the Apache License, Version 2.0.
    https://aws.amazon.com/apache2.0/

Otherwise, the modifications to this code, and all the code in the /lib directory, are copyrighted @ DKaAnG 2025.  

GitHub Repository: https://github.com/dkaang/SPL_Twitch-Bot  
"""

from irc.bot import SingleServerIRCBot
from requests import get

from src import cmds, db, react

from dotenv import dotenv_values

NAME = "mithkoeln" #dkaangg
OWNER = "mithkoeln" #dkaangg
stream_link = f"https://twitch.tv/{OWNER}"

config = dotenv_values(".env") # for the CLIENT_ID and ACCESS_TOKEN


class Bot(SingleServerIRCBot):
    def __init__(self):
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.USERNAME = NAME.lower()
        self.CLIENT_ID = config["CLIENT_ID"]
        self.TOKEN = config["ACCESS_TOKEN"]

        self.CHANNEL = f"#{OWNER}"

        url = f"https://api.twitch.tv/helix/users?login={self.USERNAME}"
        headers = {"Client-ID": self.CLIENT_ID, "Authorization": f"Bearer {self.TOKEN}"}
        try:
            response = get(url, headers=headers)
            response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
            data = response.json()
            self.channel_id = data["data"][0]["id"]
        except Exception as e:
            print("Error occured:", e)

        super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

    def on_welcome(self, connection, event):
        for req in ("membership", "tags", "commands"):
            connection.cap("REQ", f":twitch.tv/{req}")

        connection.join(self.CHANNEL)
        db.build()

        self.send_message("🤖 SPL-Bot jetzt online. 🤖")
        print(f"----- Bot online ----- \n{stream_link}")
    
    @db.with_commit # save every comment to the database
    def on_pubmsg(self, connection, event):
        tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags} # "kvpair" = key value pair
        user = {"name": tags["display-name"], "id": tags["user-id"]}
        message = event.arguments[0]
        message = message.strip()
        message = message.replace(" 󠀀", "")

        print(f"Message from {user['name']}: '{message}'")
        if user["name"] != NAME: # if the user/chatter is not the bot
            react.process(bot, user, message)
            cmds.process(bot, user, message)

    def send_message(self, message):
        self.connection.privmsg(self.CHANNEL, message.replace("\n", "").replace("\r", "")) # replace newlines)(\n) and carriage (\r) returns with empty strings

if __name__ == "__main__":
    bot = Bot()
    bot.start()

    


##### FOR TEST PURPOSES #####
# import requests
#
# url = "https://id.twitch.tv/oauth2/validate"
# headers = {"Authorization": f"Bearer q5avrmxf18cq8v4h54cqlv9rs4a9ex"}
#
# response = requests.get(url, headers=headers)
# print(response.json())
#############################