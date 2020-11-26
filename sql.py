import sqlite3

def cc(filname):
	conn = None
	conn = sqlite3.connect(filename)
	return conn

def getkeywords(conn, id):
	cur = conn.cursor()
	cur.execute("SELECT keyword FROM keywords")
	return list(cur.fetchall())

def getillegals(conn, id):
	cur = conn.cursor()
	cur.execute("SELECT illegal FROM illegals")
	return list(cur.fetchall())

def getpos(conn, id):
	cur = conn.cursor()
	cur.execute("SELECT rowid FROM corder WHERE id={}".format(id))
	return cur.fetchall() - 1

def getcommands(conn):
	cur = conn.cursor()
	cur.execute("SELECT * FROM commands")
	commands = cur.fetchall()
	cur.execute("SELECT * FROM commands")
	commands = cur.fetchall()

	final = [None] * len(commands)

	#obj = {
	#"id":0,
	#"name":"",
	#"keywordz":"",
	#"illegal":[],
	#"content":"",
	#"type":"",
	#"inside":False,
	#"all":False,
	#"admin":False
	#}

	obj = {}

	for row in commands:
		obj["id"] = str(row[0])
		obj["name"] = str(row[1])
		obj["content"] = str(row[2])
		obj["type"] = str(row[3])
		obj["keywords"] = getkeywords(conn, obj["id"])
		obj["illegal"] = getillegals(conn, obj["id"])
		obj["inside"] = bool(row[4])
		obj["all"] = bool(row[5])
		obj["admin"] = bool(row[6])
		final[getpos(conn, obj["id"])] = obj

	return final

def getstats(conn):
	cur = conn.cursor()
	cur.execute("SELECT * FROM commands")
	stats = cur.fetchall()
	return {"timesrestarted":stats[0], "messagessen":stats[1]}

def getstatus(conn):
	cur = conn.cursor()
	cur.execute("SELECT status FROM status")
	return(str(cur.fetchall()))
