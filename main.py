import discord
import os
import random
from replit import db
from keep_alive import keep_alive
import time
import asyncio
from util_functions import get_quote, get_review, update_encouragement, delete_encouragement

    
client = discord.Client()
key_words = ["sad", "depressed", "unhappy", "angry", 
            "miserable", "depressing"]
channels = ["commands"] 
joined = messages = 0
starter_encourage= ["Cheer up!", "Hang in there.", 
                   "You've got this!"]
if "responding" not in db.keys():
    db["responding"] = True

        
async def update_stats():
    #function to log information to a file called stats.txt
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {int(time.time())} Messages: {messages} Users Joined: {joined}\n")
            messages =  joined = 0
            await asyncio.sleep(43200) #log every 12 hours 
        except Exception as e:
            print(e)
            await asyncio.sleep(43200) 
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    

@client.event
async def on_member_join(member):
    global joined
    joined +=1
    for channel in member.server.channels:
        if str(channel) == "general":
            await client.send_message(f"Welcome here {member.mention}")

@client.event
async def on_message(message):
    global messages
    messages +=1

    server_id = client.get_guild(int(os.getenv("server_id")))
    
    if str(message.channel) in channels: 
        #allow commands in specific channels
        if message.author == client.user:
            return
        msg = message.content
        if msg.startswith('$inspire'):
            quote = get_quote()
            await message.channel.send(quote)
        if db["responding"]: 
            if "encouragements" in db.keys():
                options = list(db["encouragements"])
                for msg_encourage in starter_encourage:
                    options.append(msg_encourage)
            if any(word in msg for word in key_words):
                await message.channel.send(random.choice(options))
        if msg.startswith("$new"):
            new_message = msg.split("$new ", 1)[1]
            update_encouragement(new_message)
            await message.channel.send("New Encouraging Message Added.")
        if msg.startswith("$del"):
            encouragements = []
            if "encouragements" in db.keys():
                index = int(msg.split("$del ", 1)[1])
                delete_encouragement(index)
                encouragements = list(db["encouragements"])
            await message.channel.send(encouragements)
        if msg.startswith("$review"):
            book_title = msg.split("$review ", 1)[1]
            book_review = get_review(book_title)
            if book_review is None:
                await message.channel.send("No Review Found!")
            else: 
                await message.channel.send(book_review)
        if msg.startswith("$users"):
            await message.channel.send(f"# of users: {server_id.member_count}")
        if msg.startswith("$help"):
            embed = discord.Embed(title = "BOT Help", description= "Useful Commands")
            embed.add_field(name="$inspire", value="Get an inspirational quote")
            embed.add_field(name="$review book_title", value = "Get an NYT review of the book_title")
            embed.add_field(name="$users", value="See the number of users in the server")

            await message.channel.send(content = None, embed=embed)
            
        if msg.startswith("$list"):
            encouragements = starter_encourage
            if "encouragements" in db.keys():
                encouragements = encouragements+list(db["encouragements"])
            await message.channel.send(encouragements)
    
        if msg.startswith("$responding"):
            value = msg.split("$responding ", 1)[1]
            if value.lower() == "true":
                db["responding"] = True
                await message.channel.send("Responding is on")
            else:
                db["responding"] = False
                await message.channel.send("Responding is off")

keep_alive()
client.loop.create_task(update_stats())

client.run(os.getenv('TOKEN'))

