import sql
import discord

def reload():
	return discord.Embed(title = "database reloaded", color = discord.Color.from_rgb(209, 170, 88))

def restart():
	return discord.Embed(title = "dogebot restarting", color = discord.Color.from_rgb(209, 170, 88))

def addcom(conn, message):
	newcom = message.content.splitlines()
	if(not(newcom[1] and newcom[2] and newcom[3] and newcom[6] and newcom[7] and newcom[8])):
		embed = discord.Embed(title = "missing info", color = discord.Color.from_rgb(209, 170, 88))
		return embed
	if not newcom[4]:
		newcom[4] = []
	else:
		newcom[4] = newcom[4].split("|")
	if not newcom[5]:
		newcom[5] = []
	else:
		newcom[5] = newcom[5].split("|")
	for num in range(6,9):
		if newcom[num] == "yes":
			newcom[num] = True
		else:
			newcom[num] = False
	sql.addcom(conn, newcom[1], newcom[3], newcom[2], newcom[6], newcom[7], newcom[8], newcom[4], newcom[5])
	embed = discord.Embed(title = "command added", color = discord.Color.from_rgb(209, 170, 88))
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
	print(mcommands)
	for command in mcommands:
		if command["type"] not in types:
			command["type"] = "control"
		types[command["type"]].append(command)
	for type in types:
		value = ""
		for comamnd in type:
			extra = ""
			if command["admin"]:
				extra = " 🟥 "
			value = value + command["name"] + extra + "\n"
		value = value[:len(value) - 1]
		embed.add_field(name = type, value = value, inline = False)
	embed.set_thumbnail(url = message.guild.me.avatar_url)
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
		keywords = keywords[:len(keywords) - 1]
		illegals = ""
		for illegal in tcommand["illegal"]:
			illegals = illegals + illegal + " | "
		illegals = illegals[0:len(illegals) - 1]
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
