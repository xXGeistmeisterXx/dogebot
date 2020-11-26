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

def getstats(message, conn):
	print("got here")
	stats = sql.getstats(conn)
	embed = discord.Embed(title = "dogebot stats", color = discord.Color.white)
	embed.add_field(name = "messages sent", value = str(stats["messagessen"]), inline = True)
	embed.add_field(name = "times restarted", value = str(stats["timesrestarted"]), inline = True)
	embed.set_thumbnail(url = message.guild.me.avatar_url)
	return embed
