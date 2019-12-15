import discord
import os
import requests
import json
import time
from keep_alive import keep_alive

client = discord.Client()
keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")

def run(message, command):
    
    now = time.strftime('%H:%M %m/%d/%Y')
    print("[%s] %s activated %s (%s)" % (now, message.author.name, command["name"], message.guild.name))
    #addtotalms()
    
    if(command["type"] == "file"):
        
        myfile = discord.File(command["content"], filename=command["content"])
        message.channel.send(file=myfile)
        
    elif(command["type"] == "text"):
        
        message.channel.send(command["content"])
        
    elif(command["type"] == "reaction"):
        
        for emoji in command["content"]:
            
            message.add_reaction(emjoi)
        
    elif(command["type"] == "command"):
        
        result = ""
        
        for index in command["content"][1]:
            
            command["content"][0][index] = eval(message["content"][0][index])
            
        for index in command["content"][2]:
            
            result = result + str(command["content"][0][index])
            
        message.channel.send("result")
        

commands = [
    {
        "name":"doge",
        "keywordz":["doge"],
        "all":True,
        "illegal":["dogebot"],
        "inside":True,
        "type":"file",
        "content":"doge.png"
    },
    {
        "name":"bruh moment",
        "keywordz":["bruh"],
        "all":True,
        "illegal":[],
        "inside":True,
        "type":"file",
        "content":"bruh.jpeg"
    },
    {
        "name":"peter griffin",
        "keywordz":["peter", "griffin"],
        "all":True,
        "illegal":[],
        "inside":True,
        "type":"file",
        "content":"petergriffin.png"
    },
    {
        "name":"creeper",
        "keywordz":["bruh"],
        "all":True,
        "illegal":[],
        "inside":True,
        "type":"file",
        "content":"creeper.jpg"
    },
    {
        "name":"fur missile",
        "keywordz":["fur", "missile"],
        "all":True,
        "illegal":[],
        "inside":True,
        "type":"file",
        "content":"furmissile.png"
    },
    {
        "name":"problem",
        "keywordz":["problem"],
        "all":True,
        "illegal":[],
        "inside":True,
        "type":"file",
        "content":"trollface.jpg"
    },
    {
        "name":"bork bork nom nom",
        "keywordz":["bork bork nom nom"],
        "all":True,
        "illegal":[],
        "inside":True,
        "type":"file",
        "content":"borkdog.jpg"
    },
    {
        "name":"aw man",
        "keywordz":["aw", "man"],
        "all":True,
        "illegal":[],
        "inside":True,
        "type":"text",
        "content":"so we back in the mine"
    },
    {
        "name":"rap god",
        "keywordz":["rap", "god"],
        "all":True,
        "illegal":[],
        "inside":False,
        "type":"text",
        "content":">>> Dig up diamonds and craft those diamonds\nAnd make some armor, get it, baby\nGo and forge that like you so MLG pro\nThe sword's made of diamonds, so come at me, bro, huh\nTraining in your room under the torchlight\nHone that form to get you ready for the big fight\nEvery single day and the whole night\nCreeper's out prowlin', hoo, alright\nLook at me, look at you\nTake my revenge, that's what I'm gonna do\nI'm a warrior, baby, what else is new?\nAnd my blade's gonna tear through you, bring it\n**~CaptainSparklez**"
    },
    {
        "name":"dab",
        "keywordz":["dab"],
        "all":True,
        "illegal":[],
        "inside":True,
        "type":"text",
        "content":"<o/"
    },
    {
        "name":"^",
        "keywordz":["^"],
        "all":True,
        "illegal":[],
        "inside":False,
        "type":"text",
        "content":"^"
    },
    {
        "name":"raider rumble",
        "keywordz":["raider"],
        "all":True,
        "illegal":[],
        "inside":False,
        "type":"text",
        "content":"rumble"
    },
    {
        "name":"welcome to Moes",
        "keywordz":["welcome to"],
        "all":True,
        "illegal":[],
        "inside":False,
        "type":"text",
        "content":"Moes"
    },
    {
        "name":"bork",
        "keywordz":["bork"],
        "all":True,
        "illegal":["nom"],
        "inside":True,
        "type":"reaction",
        "content":["🇧", "🇴", "🇷", "🇰"]
    },
    {
        "name":"nom",
        "keywordz":["nom"],
        "all":True,
        "illegal":["bork"],
        "inside":True,
        "type":"reaction",
        "content":["🇳", "🇴", "🇲"]
    },
    {
        "name":"bork nom",
        "keywordz":["bork", "nom"],
        "all":True,
        "illegal":[],
        "inside":True,
        "type":"reaction",
        "content":["🐩"]
    },
    {
        "name":"yam",
        "keywordz":["yam"],
        "all":True,
        "illegal":[],
        "inside":True,
        "type":"reaction",
        "content":["🍠"]
    },
    {
        "name":"eggplant",
        "keywordz":["69", "420", "penis", "dick"],
        "all":False,
        "illegal":[],
        "inside":True,
        "type":"reaction",
        "content":["🍆"]
    },
    {
        "name":"@dogebot",
        "keywordz":["<@612070962913083405>"],
        "all":True,
        "illegal":[],
        "inside":True,
        "type":"command",
        "content":(["<@", "message.author.id", ">"], [1], [0,1,2])
    },
    {
        "name":"help",
        "keywordz":["dogebot.help", "dogebot.commands"],
        "all":False,
        "illegal":[],
        "inside":False,
        "type":"command",
        "content":(["getcommands()"], [0], [0])
    }]
    
jcommands = '[{"name": "doge", "keywordz": ["doge"], "all": true, "illegal": ["dogebot"], "inside": true, "type": "file", "content": "doge.png"}, {"name": "bruh moment", "keywordz": ["bruh"], "all": true, "illegal": [], "inside": true, "type": "file", "content": "bruh.jpeg"}, {"name": "peter griffin", "keywordz": ["peter", "griffin"], "all": true, "illegal": [], "inside": true, "type": "file", "content": "petergriffin.png"}, {"name": "creeper", "keywordz": ["bruh"], "all": true, "illegal": [], "inside": true, "type": "file", "content": "creeper.jpg"}, {"name": "fur missile", "keywordz": ["fur", "missile"], "all": true, "illegal": [], "inside": true, "type": "file", "content": "furmissile.png"}, {"name": "problem", "keywordz": ["problem"], "all": true, "illegal": [], "inside": true, "type": "file", "content": "trollface.jpg"}, {"name": "bork bork nom nom", "keywordz": ["bork bork nom nom"], "all": true, "illegal": [], "inside": true, "type": "file", "content": "borkdog.jpg"}, {"name": "aw man", "keywordz": ["aw", "man"], "all": true, "illegal": [], "inside": true, "type": "text", "content": "so we back in the mine"}, {"name": "rap god", "keywordz": ["rap", "god"], "all": true, "illegal": [], "inside": false, "type": "text", "content": ">>> Dig up diamonds and craft those diamonds\nAnd make some armor, get it, baby\nGo and forge that like you so MLG pro\nThe sword\'s made of diamonds, so come at me, bro, huh\nTraining in your room under the torchlight\nHone that form to get you ready for the big fight\nEvery single day and the whole night\nCreeper\'s out prowlin\', hoo, alright\nLook at me, look at you\nTake my revenge, that\'s what I\'m gonna do\nI\'m a warrior, baby, what else is new?\nAnd my blade\'s gonna tear through you, bring it\n**~CaptainSparklez**"}, {"name": "dab", "keywordz": ["dab"], "all": true, "illegal": [], "inside": true, "type": "text", "content": "<o/"}, {"name": "^", "keywordz": ["^"], "all": true, "illegal": [], "inside": false, "type": "text", "content": "^"}, {"name": "raider rumble", "keywordz": ["raider"], "all": true, "illegal": [], "inside": false, "type": "text", "content": "rumble"}, {"name": "welcome to Moes", "keywordz": ["welcome to"], "all": true, "illegal": [], "inside": false, "type": "text", "content": "Moes"}, {"name": "bork", "keywordz": ["bork"], "all": true, "illegal": ["nom"], "inside": true, "type": "reaction", "content": ["\ud83c\udde7", "\ud83c\uddf4", "\ud83c\uddf7", "\ud83c\uddf0"]}, {"name": "nom", "keywordz": ["nom"], "all": true, "illegal": ["bork"], "inside": true, "type": "reaction", "content": ["\ud83c\uddf3", "\ud83c\uddf4", "\ud83c\uddf2"]}, {"name": "bork nom", "keywordz": ["bork", "nom"], "all": true, "illegal": [], "inside": true, "type": "reaction", "content": ["\ud83d\udc29"]}, {"name": "yam", "keywordz": ["yam"], "all": true, "illegal": [], "inside": true, "type": "reaction", "content": ["\ud83c\udf60"]}, {"name": "eggplant", "keywordz": ["69", "420", "penis", "dick"], "all": false, "illegal": [], "inside": true, "type": "reaction", "content": ["\ud83c\udf46"]}, {"name": "@dogebot", "keywordz": ["<@612070962913083405>"], "all": true, "illegal": [], "inside": true, "type": "command", "content": [["<@", "message.author.id", ">"], [1], [0, 1, 2]]}, {"name": "help", "keywordz": ["dogebot.help", "dogebot.commands"], "all": false, "illegal": [], "inside": false, "type": "command", "content": [["getcommands()"], [0], [0]]}]'

print(str(discord.__version__) + " is the discord.py version")
print("")

@client.event
async def on_message(message):
    
    if(not message.author.bot):
    
        for command in commands:
            notillegal = True
            for illegal in command["illegal"]:
                if illegal in message.content.lower():
                    notillegal = False
            if(notillegal):
                if(command["inside"] == True):
                    for keyword in command["keywordz"]:
                        if(keyword in message.content.lower()):
                            await run(message, command)
                else:
                    for keyword in command["keywordz"]:
                        if(keyword == message.content.lower()):
                            await run(message, command)

client.run(token)
