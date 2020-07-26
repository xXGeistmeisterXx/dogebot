import discord
import os
import requests
import json
import time
import sys
import asyncio
import threading

os.system("clear")

admins = ["355803584228622346"]

game = "dogebot.help"

def log(content):
        f = open("doge.log", "a")
        now = time.strftime('%H:%M %m/%d/%Y')
        content = "[%s] %s\n" % (now, content)
        f.write(content)
        f.close()

def getcommands(offline, content=None):
	result = ""
	if(not offline and len(content.split()) > 1 and content.split()[0] in ["dogebot.help", "dogebot.commands"]):
		com = ""
		for i in range(len(content.split())):
			if i > 0:
				com = com + content.split()[i] + " "
		for command in commands:
			if command["name"] == com[0:len(com) - 1]:
				return(json.dumps(command))
		return("`COMMAND NOT FOUND`")
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
	f = open("commands.json", "w")
	f.write(json.dumps(commands))
	f.close()

def upcommand(command):
	for i in range(len(commands)):
		if(commands[i]["name"] == command["name"]):
			commands[i] = command
			f = open("commands.json", "w")
			f.write(json.dumps(commands))
			f.close()
			return()

def delcommand(command):
	for i in range(len(commands)):
		if(commands[i]["name"] == command["name"]):
			del commands[i]
			f = open("commands.json", "w")
			f.write(json.dumps(commands))
			f.close()

def anummessent():
	stats["messagessen"] += 1
	f = open("stats.json", "w")
	f.write(json.dumps(stats))
	f.close()

def anumres():
	stats["timesrestarted"] += 1
	f = open("stats.json", "w")
	f.write(json.dumps(stats))
	f.close()

def usercommands(message, ctype):

	length = len(message.content.split()[0])
	command = message.content[length + 1:]

	if(ctype == "add"):

		addcommand(json.loads(command))
		log("added " + json.loads(command)["name"])

	elif(ctype == "update"):

		upcommand(json.loads(command))
		log("updated " + json.loads(command)["name"])

	elif(ctype == "delete"):

		delcommand(json.loads(command))
		log("deleted " + json.loads(command)["name"])

	return("commands db updated successfully")

def changescore(name, num):
  f = open("scoreboard.json", "r")
  scoreboard = json.loads(f.readline())
  f.close()
  score = scoreboard[name] if name in scoreboard else 0
  score += num
  scoreboard[name] = score
  f = open("scoreboard.json", "w")
  f.write(json.dumps(scoreboard))
  f.close()
  return score

def changescoref(content):
  return "`changed " + content.split()[1] + " to " + str(changescore(content.split()[1], int (content.split()[2]))) + "`"

def delscore(name):
  f = open("scoreboard.json", "r")
  scoreboard = json.loads(f.readline())
  f.close()
  if name in scoreboard:
    del scoreboard[name]
  f = open("scoreboard.json", "w")
  f.write(json.dumps(scoreboard))
  f.close()

def delscoref(content):
  delscore(content.split()[1])
  return "`deleted " + content.split()[1] + "`"

def getscore():
  f = open("scoreboard.json", "r")
  scoreboard = json.loads(f.readline())
  f.close()
  return scoreboard

def getscoref():
  scoreboard = getscore()
  scoreboard = {k: v for k, v in sorted(scoreboard.items(), key=lambda item: item[1], reverse=True)}
  result = "```SCOREBOARD:\n"
  for name in scoreboard:
    result = result + name + " : " + str(scoreboard[name]) + "\n"
  if(len(scoreboard) < 1):
    return "`EMPTY`"
  return result + "```"

client = discord.Client()
f = open("token.txt", "r")
token = f.readline()
f.close()
#token = os.environ.get("DISCORD_BOT_SECRET")

file = open("commands.json", "r")
commands = json.loads(file.readline())
file.close()
file = open("stats.json", "r")
stats = json.loads(file.readline())
file.close()

async def setgame():
	await client.wait_until_ready()
	await client.change_presence(activity=discord.Game(name=game))

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
			log("(%s) %s activated %s" % (message.guild.name, message.author.name, com["name"]))
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

log("STARTED DOGEBOT")
client.loop.create_task(setgame())
client.run(token)
