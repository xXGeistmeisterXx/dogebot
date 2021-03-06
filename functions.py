import sql
import discord
import copy

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
	sql.updatecom(conn, upcom[0], upcom[1], upcom[3], upcom[2], upcom[6], upcom[7], upcom[8], upcom[4], upcom[5])
	embed = discord.Embed(title = "command updated", color = discord.Color.from_rgb(209, 170, 88))
	return embed

def deletecom(conn, message, commands):
	upcom = message.content.splitlines()
	flag = False
	for command in commands:
		if upcom[1] == str(command["id"]):
			flag = True
			break
	if not flag:
		embed = discord.Embed(title = "command not found", color = discord.Color.from_rgb(209, 170, 88))
		return embed
	sql.deletecom(conn, upcom[1])
	embed = discord.Embed(title = "command deleted", color = discord.Color.from_rgb(209, 170, 88))
	return embed

def addadmin(conn, message, admins):
	dcid = 0
	try:
		dcid = int(message.content.split()[1])
	except:
		return discord.Embed(title = "invalid id format", color = discord.Color.from_rgb(209, 170, 88))
	if dcid in admins:
		return discord.Embed(title = "already admin", color = discord.Color.from_rgb(209, 170, 88))
	sql.addadmin(conn, dcid)
	return discord.Embed(title = "admin added", color = discord.Color.from_rgb(209, 170, 88))

def deleteadmin(conn, message, admins):
	dcid = 0
	try:
		dcid = int(message.content.split()[1])
	except:
		return discord.Embed(title = "invalid id format", color = discord.Color.from_rgb(209, 170, 88))
	if dcid not in admins:
		return discord.Embed(title = "not admin", color = discord.Color.from_rgb(209, 170, 88))
	sql.deleteadmin(conn, dcid)
	return discord.Embed(title = "admin deleted", color = discord.Color.from_rgb(209, 170, 88))

def addban(conn, message, bans):
	dcid = 0
	try:
		dcid = int(message.content.split()[1])
	except:
		return discord.Embed(title = "invalid id format", color = discord.Color.from_rgb(209, 170, 88))
	if dcid in bans:
		return discord.Embed(title = "already banned", color = discord.Color.from_rgb(209, 170, 88))
	sql.addban(conn, dcid)
	return discord.Embed(title = "banned", color = discord.Color.from_rgb(209, 170, 88))

def deleteban(conn, message, bans):
	dcid = 0
	try:
		dcid = int(message.content.split()[1])
	except:
		return discord.Embed(title = "invalid id format", color = discord.Color.from_rgb(209, 170, 88))
	if dcid not in bans:
		return discord.Embed(title = "not banned", color = discord.Color.from_rgb(209, 170, 88))
	sql.deleteban(conn, dcid)
	return discord.Embed(title = "unbanned", color = discord.Color.from_rgb(209, 170, 88))

def getstats(message, stats):
	embed = discord.Embed(title = "stats", color = discord.Color.from_rgb(209, 170, 88))
	embed.add_field(name = "messages sent", value = str(stats["messagessen"]), inline = True)
	embed.add_field(name = "times restarted", value = str(stats["timesrestarted"]), inline = True)
	embed.set_thumbnail(url = message.guild.me.avatar_url)
	return embed

def getcoms(message, commands):
	embed = discord.Embed(title = "commands", color = discord.Color.from_rgb(209, 170, 88))
	mcommands = copy.deepcopy(commands)
	types = {
	"text":[],
	"reaction":[],
	"file":[],
	"embed":[],
	"command":[],
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
			value = value + extra + command["name"] + "\n"
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


def alphatwin(message):
	embed = discord.Embed(title = "THE ALPHA TWIN IS...", description= "BEN", color = discord.Color.from_rgb(209, 170, 88))
	embed.set_thumbnail(url = "https://imgur.com/xvvcuHB.png")
	return embed

def at(message):
	return("<@{}>".format(message.author.id))
