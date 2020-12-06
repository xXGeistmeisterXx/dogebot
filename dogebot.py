import discord
import os
import json
import time
import asyncio
import sqlite3
import sql
import functions

os.system("clear")

dbfile = "db/doge.db"
dbcc = sql.cc(dbfile)

def log(content):
		f = open("doge.log", "a")
		now = time.strftime('%H:%M %m/%d/%Y')
		content = "[%s] %s\n" % (now, content)
		f.write(content)
		f.close()

def anummessent():
	stats["messagessen"] += 1
	sql.updatemessages(dbcc, stats)

def anumres():
	stats["timesrestarted"] += 1
	sql.updaterestarts(dbcc, stats)

client = discord.Client()
f = open("token.txt", "r")
token = f.readline()
f.close()

commands = sql.getcommands(dbcc)
admins = sql.getadmins(dbcc)
stats = sql.getstats(dbcc)
game = sql.getstatus(dbcc)
bans = sql.getbans(dbcc)
anumres()

async def setgame():
	await client.wait_until_ready()
	await client.change_presence(activity=discord.Game(name=game))

@client.event
async def on_message(message):
	global commands, admins, stats, game, bans
	com = None
	if(not message.author.bot and message.author.id not in bans):
		for command in commands:
			print(command)
			notillegal = True
			for illegal in command["illegal"]:
				if illegal in message.content.lower():
					notillegal = False
			if(notillegal and ((command["admin"] and (message.author.id in admins)) or (not command["admin"]))):
				if(command["inside"]):
					if(command["all"]):
						check = True
						for keyword in command["keywords"]:
							if(not(keyword in message.content.lower())):
								check = False
						if(check):
							com = command
					else:
						for keyword in command["keywords"]:
							if(keyword in message.content.lower()):
								com = command
				else:
					for keyword in command["keywords"]:
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

			elif(com["type"] == "embed"):

				result = eval("functions." + str(com["content"]))
				await message.channel.send(embed=result)

			elif(com["type"] == "command"):

				result = eval("functions." + str(com["content"]))
				await message.channel.send(result)

			elif(com["type"] == "restart"):
				results = functions.restart()
				await message.channel.send(embed=results)
				os.system("/home/tgeist/update.sh")
				print("ran")

			elif(com["type"] == "reload"):
				commands = sql.getcommands(dbcc)
				admins = sql.getadmins(dbcc)
				stats = sql.getstats(dbcc)
				game = sql.getstatus(dbcc)
				bans = sql.getbans(dbcc)
				results = functions.reload()
				await message.channel.send(embed=results)

log("STARTED DOGEBOT")
client.loop.create_task(setgame())
client.run(token)
