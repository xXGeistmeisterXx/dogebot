import discord
import os
import requests
import json
import time
import sys
from keep_alive import keep_alive

admins = ["355803584228622346"]

def restart():
    os.execl(sys.executable, sys.executable, * sys.argv)
    return("restarting")

def getcommands(offline):
    result = ""
    if(offline):
        result = "```dogebot commands (offline):\n"
    else:
        result = "```dogebot commands:\n"
    for command in commands:
        result = result + " - " + command["name"] + "\n"
    return(result + "```")

def getstats():
    result = "```dogebot stats:\n"
    result = result + " - times restarted: " + str(stats["timesrestarted"]) + "\n"
    result = result + " - number of messages sent: " + str(stats["messagessen"])
    return(result + "```")

def addcommand(command):
    for ocommand in commands:
        if(ocommand["name"] == command["name"]):
            return()
    commands.append(command)
    r = requests.post(url = URL + "/commands", json = json.dumps(commands))

def upcommand(command):
    for i in range(len(commands)):
        if(commands[i]["name"] == command["name"]):
            commands[i] = command
            r = requests.post(url = URL + "/commands", json = json.dumps(commands))
            return()

def delcommand(command):
    for i in range(len(commands)):
        if(commands[i]["name"] == command["name"]):
            del commands[i]
            r = requests.post(url = URL + "/commands", json = json.dumps(commands))
    
def anummessent():
    stats["messagessen"] += 1
    requests.post(url = URL + "/stats", json = json.dumps(stats))

def anumres():
    stats["timesrestarted"] += 1
    requests.post(url = URL + "/stats", json = json.dumps(stats))

def usercommands(message, ctype):
    command = "".join(message.content.split()[1:len(message.content.split())])

    if(ctype == "add"):
        
        addcommand(json.loads(command))
        print("added " + json.loads(command)["name"])
        
    elif(ctype == "update"):
        
        upcommand(json.loads(command))
        print("updated " + json.loads(command)["name"])
        
    elif(ctype == "delete"):
        
        delcommand(json.loads(command))
        print("deleted " + json.loads(command)["name"])
    
    return("commands db updated successfully")
    


client = discord.Client()
keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
URL = os.environ.get("URL")

#file = open("archive.json", "r")
#obj = json.loads(file.readline())
#commands = json.dumps(obj[0])
#stats = json.dumps(obj[1])
#file.close()
#requests.post(url = URL + "/commands", json = str(commands))
#requests.post(url = URL + "/stats", json = stats)

borked = False
try:
    commands = json.loads(requests.get(url = URL + "/commands").json()["result"])
except:
    file = open("defaults.json", "r")
    commands = json.loads(file.readline())[0]
    file.close()
    borked = True

try:
    stats = json.loads(requests.get(url = URL + "/stats").json()["result"])
except:
    file = open("defaults.json", "r")
    stats = json.loads(file.readline())[1]
    file.close()
    borked = True

if(not borked):
    anumres()

@client.event
async def on_message(message):
    com = None
    if(not message.author.bot):
    
        for command in commands:
            notillegal = True
            for illegal in command["illegal"]:
                if illegal in message.content.lower():
                    notillegal = False
            if(notillegal and ((command["admin"] and (str(message.author.id) in admins)) or (not command["admin"]))):
                if(command["inside"]):
                    if(command["all"]):
                        check = True
                        for keyword in command["keywordz"]:
                            if(not(keyword in message.content.lower())):
                                check = False
                        if(check):
                            com = command
                    else:
                        for keyword in command["keywordz"]:
                            if(keyword in message.content.lower()):
                                com = command
                else:
                    for keyword in command["keywordz"]:
                        if(keyword == message.content.lower()):
                            com = command
        
        if(com):
            now = time.strftime('%H:%M %m/%d/%Y')
            print("[%s] (%s) %s activated %s" % (now, message.guild.name, message.author.name, com["name"]))
            if(not borked):
                anummessent()
            
            if(com["type"] == "file"):
                
                myfile = discord.File("files/" + com["content"], filename=com["content"])
                await message.channel.send(file=myfile)
                
            elif(com["type"] == "text"):
                
                await message.channel.send(com["content"])
                
            elif(com["type"] == "reaction"):
                
                for emoji in com["content"]:
                    
                    await message.add_reaction(emoji)
                
            elif(com["type"] == "command"):
                
                result = ""
                output = {}
                
                for index in com["content"][1]:
                    
                    output[index] = eval(com["content"][0][index])
                    
                for index in com["content"][2]:
                    if(not(index in com["content"][1])):
                        output[index] = com["content"][0][index]
                        
                    result = result + str(output[index])
                    
                await message.channel.send(result)

print("STARTED")                 
client.run(token)
