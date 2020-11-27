import sqlite3

dbfile = "db/doge.db"

def cc(filename):
	conn = None
	conn = sqlite3.connect(filename)
	return conn

def getkeywords(conn, id):
	conn = cc(dbfile)
	cur = conn.cursor()
	cur.execute("SELECT keyword FROM keywords WHERE id={}".format(id))
	keywords = list(cur.fetchall())
	output = []
	for keyword in keywords:
		output.append(keyword[0])
	cur.close()
	conn.close()
	return output

def getillegals(conn, id):
	conn = cc(dbfile)
	cur = conn.cursor()
	cur.execute("SELECT illegal FROM illegals WHERE id={}".format(id))
	illegals = list(cur.fetchall())
	output = []
	for illegal in illegals:
		output.append(illegal[0])
	cur.close()
	conn.close()
	return output

def getpos(conn, id):
	conn = cc(dbfile)
	cur = conn.cursor()
	cur.execute("SELECT rowid FROM corder WHERE id={}".format(id))
	output = cur.fetchall()[0][0] - 1
	cur.close()
	conn.close()
	return output

def getcommands(conn):
	conn = cc(dbfile)
	cur = conn.cursor()
	cur.execute("SELECT * FROM commands")
	commands = cur.fetchall()
	cur.execute("SELECT * FROM commands")
	commands = cur.fetchall()
	cur.close()
	conn.close()

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
	conn = cc(dbfile)
	cur = conn.cursor()
	cur.execute("SELECT * FROM stats")
	stats = cur.fetchall()
	cur.close()
	conn.close()
	return {"timesrestarted":stats[0][0], "messagessen":stats[0][1]}

def getstatus(conn):
	conn = cc(dbfile)
	cur = conn.cursor()
	cur.execute("SELECT status FROM status")
	output = cur.fetchall()[0][0]
	cur.close()
	conn.close()
	return output

def getadmins(conn):
	conn = cc(dbfile)
	cur = conn.cursor()
	cur.execute("SELECT dcid FROM admins")
	admins = list(cur.fetchall())
	output = []
	for admin in admins:
		output.append(int(admin[0]))
	cur.close()
	conn.close()
	return output

def updatemessages(conn, stats):
	conn = cc(dbfile)
	stats = getstats(conn)
	cur = conn.cursor()
	cur.execute("UPDATE stats SET messages = {} WHERE rowid = 1;".format(stats["messagessen"]))
<<<<<<< HEAD
	print("UPDATE stats SET messages = {} WHERE rowid = 1;".format(stats["messagessen"]))
	conn.commit()
	cur.close()
	conn.close()
=======
>>>>>>> parent of f484bb9... tadaa

def updaterestarts(conn, stats):
	conn = cc(dbfile)
	stats = getstats(conn)
	cur = conn.cursor()
	cur.execute("UPDATE stats SET restarts = {} WHERE rowid = 1;".format(stats["timesrestarted"]))
<<<<<<< HEAD
	conn.commit()
	cur.close()
	conn.close()
=======
>>>>>>> parent of f484bb9... tadaa
