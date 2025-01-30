from .. import db
from time import time

superUserID = "125313114" # yung yoom

# Dictionary to store votes: {user_id: choice}
votes = {}

availableVotes = []

voteActive = False

def vote_start(bot, user, *args):
    global voteActive, availableVotes, votes
    print(user)
    print(user["id"])

    if user["id"] != superUserID:
        bot.send_message(f"{user['name']}, you are not authorized to use this command.")
        return
    
    if len(args) < 2:
        bot.send_message("Please use: !votestart <option1> <option2> ...")
        return
    
    votes.clear()
    availableVotes.clear()
    
    voteActive = True
    
    for arg in args:
        availableVotes.append(arg.title())
        
    print(availableVotes)
    
    bot.send_message(f"Vote started! Options: {', '.join(availableVotes)}. \nUse !vote <option> to vote.")


def vote_end(bot, user, *args):
    global voteActive, availableVotes, votes
    if user["id"] != superUserID:
        bot.send_message(f"{user['name']}, you are not authorized to use this command.")
        return
    
    if not voteActive:
        bot.send_message("No vote is currently active.")
        return
    
    voteActive = False
    
    if not votes:
        bot.send_message("No votes were cast.")
        return
    
    voteCount = {}
    
    for vote in votes.values():
        if vote not in voteCount:
            voteCount[vote] = 1
        else:
            voteCount[vote] += 1
    
    winner = max(voteCount, key=voteCount.get)
    votes_for_winner = voteCount[winner]
    bot.send_message(f"Vote ended! Winner: {winner.title()} with {votes_for_winner} votes!")

    for option in voteCount:
        count = voteCount[option]
        print(f"{option.title()}: {count} votes")
    
    votes.clear()
    availableVotes.clear()


def vote(bot, user, *args):
    global voteActive, availableVotes, votes
    
    if voteActive is None or availableVotes is None or votes is None:
        voteActive = False
        availableVotes = []
        votes = {}
    
    if not availableVotes:
        bot.send_message("No vote is currently active.")
        return

    if voteActive == False:
        bot.send_message("No vote is currently active.")
        return

    if len(args) != 1:
        bot.send_message("Please vote using: !vote <option>")
        return

    choice = args[0]
    if choice.title() not in availableVotes:
        bot.send_message(f"Invalid option. Available options: {', '.join(availableVotes)}")
        return

    user_id = user['id']
    if user_id in votes:
        bot.send_message(f"{user['name']}, you have already voted!")
        return

    votes[user_id] = choice
    bot.send_message(f"{user['name']} voted for {choice.title()}!")