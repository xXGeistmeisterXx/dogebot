import sql
import discord

def reload():
	return discord.Embed(title = "database reloaded", color = discord.Color.from_rgb(209, 170, 88))

def restart():
	return discord.Embed(title = "dogebot restarting", color = discord.Color.from_rgb(209, 170, 88))

def docom(com):
	if(not(com[1] and com[2] and com[3] and com[6] and com[7] and com[8])):
		return False
	if not com[4]:
		com[4] = []
	else:
		com[4] = com[4].split("|")
	if not com[5]:
		com[5] = []
	else:
		com[5] = com[5].split("|")
	for num in range(6,9):
		if com[num] == "yes":
			com[num] = True
		else:
			com[num] = False
	return com

def addcom(conn, message):
	newcom = message.content.splitlines()
	newcom = docom(newcom)
	if not newcom:
		embed = discord.Embed(title = "missing info", color = discord.Color.from_rgb(209, 170, 88))
		return embed
	sql.addcom(conn, newcom[1], newcom[3], newcom[2], newcom[6], newcom[7], newcom[8], newcom[4], newcom[5])
	embed = discord.Embed(title = "command added", color = discord.Color.from_rgb(209, 170, 88))
	return embed

def updatecom(conn, message, commands):
	upcom = message.content.splitlines()
	flag = False
	for command in commands:
		if upcom[1] == str(command["id"]):
			flag = True
			break
	if not flag:
		embed = discord.Embed(title = "command not found", color = discord.Color.from_rgb(209, 170, 88))
		return embed
	upcom = docom(upcom[1:])
	if not upcom:
		embed = discord.Embed(title = "missing info", color = discord.Color.from_rgb(209, 170, 88))
		return embed
	sql.updatecom(conn, com[0], com[1], com[3], com[2], com[6], com[7], com[8], com[4], com[5])
	embed = discord.Embed(title = "command updated", color = discord.Color.from_rgb(209, 170, 88))
	return embed

def getstats(message, stats):
	embed = discord.Embed(title = "stats", color = discord.Color.from_rgb(209, 170, 88))
	embed.add_field(name = "messages sent", value = str(stats["messagessen"]), inline = True)
	embed.add_field(name = "times restarted", value = str(stats["timesrestarted"]), inline = True)
	embed.set_thumbnail(url = message.guild.me.avatar_url)
	return embed

def getcoms(message, commands):
	embed = discord.Embed(title = "commands", color = discord.Color.from_rgb(209, 170, 88))
	mcommands = commands.copy()
	types = {
	"text":[],
	"reaction":[],
	"file":[],
	"embed":[],
	"function":[],
	"control":[]
	}
	for command in mcommands:
		if command["type"] not in types:
			command["type"] = "control"
		types[command["type"]].append(command)
	for type in types:
		value = ""
		if types[type] == []:
			embed.add_field(name = type, value = "-", inline = False)
			continue
		for command in types[type]:
			extra = ""
			if command["admin"]:
				extra = " 🟥 "
			value = value + command["name"] + extra + "\n"
		value = value[:len(value) - 1]
		embed.add_field(name = type, value = value, inline = False)
	#embed.set_thumbnail(url = "message.guild.me.avatar_url")
	return embed

def em(value):
	if(value):
		return " 🟩 "
	else:
		return " 🟥 "

def getinfo(message, commands):
	content = message.content.lower().replace("db.info ", "")
	flag = False
	tcommand = {}
	for command in commands:
		if command["name"] == content:
			flag = True
			tcommand = command
			break
	if(flag):
		keywords = ""
		for keyword in tcommand["keywords"]:
			keywords = keywords + keyword + " | "
		keywords = keywords[:len(keywords) - 2]
		illegals = ""
		for illegal in tcommand["illegal"]:
			illegals = illegals + illegal + " | "
		illegals = illegals[0:len(illegals) - 2]
		if not illegals:
			illegals = "-"
		embed = discord.Embed(title = "command info", color = discord.Color.from_rgb(209, 170, 88))
		embed.add_field(name = "id", value = tcommand["id"], inline = False)
		embed.add_field(name = "name", value = tcommand["name"], inline = False)
		embed.add_field(name = "type", value = tcommand["type"], inline = False)
		embed.add_field(name = "content", value = tcommand["content"], inline = False)
		embed.add_field(name = "keywords", value = keywords, inline = False)
		embed.add_field(name = "illegal", value = illegals, inline = False)
		embed.add_field(name = "inside", value = em(tcommand["inside"]), inline = False)
		embed.add_field(name = "all", value = em(tcommand["all"]), inline = False)
		embed.add_field(name = "admin", value = em(tcommand["admin"]), inline = False)
		embed.set_thumbnail(url = message.guild.me.avatar_url)
	else:
		embed = discord.Embed(title = "command not found", color = discord.Color.from_rgb(209, 170, 88))
	return embed
