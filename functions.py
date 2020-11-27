import sql
import discord

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

def getstatsf(message):
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

def getstats(message, stats):
	embed = discord.Embed(title = "stats", color = discord.Color.from_rgb(209, 170, 88))
	embed.add_field(name = "messages sent", value = str(stats["messagessen"]), inline = True)
	embed.add_field(name = "times restarted", value = str(stats["timesrestarted"]), inline = True)
	embed.set_thumbnail(url = message.guild.me.avatar_url)
	return embed

def getcoms(message, commands):
	embed = discord.Embed(title = "commands", color = discord.Color.from_rgb(209, 170, 88))
	for command in commands:
		embed.add_field(name = command["name"], value = command["keywords"][0], inline = False)
	embed.set_thumbnail(url = message.guild.me.avatar_url)
	return embed

def em(value):
	if(value):
		return ":green_sqaure:"
	else:
		return ":red_square:"

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
			keywords = keywords + keyword + ","
		print(keywords)
		keywords = keywords[:len(keywords) - 1]
		print(keywords)
		illegals = ""
		for illegal in tcommand["illegal"]:
			illegals = illegals + illegal + ","
		illegals = illegals[0:len(illegals)-2]
		print(illegals)
		embed = discord.Embed(title = tcommand["name"], color = discord.Color.from_rgb(209, 170, 88))
		embed.add_field(name = "id", value = tcommand["id"], inline = False)
		embed.add_field(name = "name", value = tcommand["name"], inline = False)
		embed.add_field(name = "content", value = tcommand["content"], inline = False)
		embed.add_field(name = "keywords", value = keywords, inline = False)
		embed.add_field(name = "illegal", value = illegals, inline = False)
		#embed.add_field(name = "inside", value = em(tcommand["inside"]), inline = False)
		#embed.add_field(name = "all", value = em(tcommand["all"]), inline = False)
		#embed.add_field(name = "admin", value = em(tcommand["admin"]), inline = False)
		embed.set_thumbnail(url = message.guild.me.avatar_url)
	else:
		embed = discord.Embed(title = "command not found", color = discord.Color.from_rgb(209, 170, 88))
	return embed
