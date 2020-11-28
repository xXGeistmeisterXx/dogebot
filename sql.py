import sqlite3

def cc(filename):
	conn = None
	conn = sqlite3.connect(filename)
	return conn

def getkeywords(conn, id):
	cur = conn.cursor()
	cur.execute("SELECT keyword FROM keywords WHERE id={}".format(id))
	keywords = list(cur.fetchall())
	output = []
	for keyword in keywords:
		output.append(keyword[0])
	return output

def getillegals(conn, id):
	cur = conn.cursor()
	cur.execute("SELECT illegal FROM illegals WHERE id={}".format(id))
	illegals = list(cur.fetchall())
	output = []
	for illegal in illegals:
		output.append(illegal[0])
	return output

def getpos(conn, id):
	cur = conn.cursor()
	cur.execute("SELECT rowid FROM corder WHERE id={}".format(id))
	return cur.fetchall()[0][0] - 1

def getcommands(conn):
	cur = conn.cursor()
	cur.execute("SELECT * FROM commands")
	commands = cur.fetchall()
	cur.execute("SELECT * FROM commands")
	commands = cur.fetchall()

	final = [None] * len(commands)
	nobj = {}

	for row in list(commands):
		obj = nobj.copy()
		obj["id"] = str(row[0])
		obj["name"] = str(row[1])
		obj["content"] = str(row[2])
		obj["type"] = str(row[3])
		obj["keywords"] = getkeywords(conn, obj["id"])
		obj["illegal"] = getillegals(conn, obj["id"])
		obj["inside"] = bool(row[4])
		obj["all"] = bool(row[5])
		obj["admin"] = bool(row[6])
		pos = getpos(conn, obj["id"])
		final[pos] = obj

	print(final)
	return final

def getstats(conn):
	cur = conn.cursor()
	cur.execute("SELECT * FROM stats")
	stats = cur.fetchall()
	return {"timesrestarted":stats[0][0], "messagessen":stats[0][1]}

def getstatus(conn):
	cur = conn.cursor()
	cur.execute("SELECT status FROM status")
	return cur.fetchall()[0][0]

def getadmins(conn):
	cur = conn.cursor()
	cur.execute("SELECT dcid FROM admins")
	admins = list(cur.fetchall())
	output = []
	for admin in admins:
		output.append(int(admin[0]))
	return output

def addcom(conn, name, content, type, inside, all, admin, keywords, illegals, loc):
	cur = conn.cursor()
	query = "INSERT INTO commands(name,content,type,inside,'all',admin) VALUES ('{}', '{}', '{}', {}, {}, {})".format(name, content, type, int(inside), int(all), int(admin))
	cur.execute(query)
	conn.commit()
	query = "SELECT id FROM commands WHERE name='{}' AND content='{}' AND type='{}' AND inside={} AND 'all'={} AND admin={}".format(name, content, type, int(inside), int(all), int(admin))
	cur.execute(query)
	id = cur.fetchall()
	print(id)
	for keyword in keywords:
		query = "INSERT INTO keywords(id, keyword) VALUES ({},'{}')".format(id, keyword)
		cur.execute(query)
	for illegal in illegals:
		query = "INSERT INTO illegals(id, illegal) VALUES ({},'{}')".format(id, illegal)
		cur.execute(query)
	query = "SELECT id FROM corder"
	cur.execute(query)
	order = cur.fetchall()
	print(order)
	if loc > order[len(order) - 1]:
		query = "INSERT INTO corder(id) VALUES ({})".format(id)
		cur.execute(query)
	else:
		norder = [id] + order[loc-1:len(order) - 1]
		for id in norder:
			query = "UPDATE corder SET id = {} WHERE rowid = {}".format(id, loc)
			cur.execute(query)
			loc += 1
		query = "INSERT INTO corder(id) VALUES ({})".format(order[len(order) - 1])
		cur.execute(query)
	conn.commit()


def updatemessages(conn, stats):
	cur = conn.cursor()
	cur.execute("UPDATE stats SET messages = {} WHERE rowid = 1;".format(stats["messagessen"]))
	conn.commit()

def updaterestarts(conn, stats):
	cur = conn.cursor()
	cur.execute("UPDATE stats SET restarts = {} WHERE rowid = 1;".format(stats["timesrestarted"]))
	conn.commit()
