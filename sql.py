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

def getcommands(conn):
	cur = conn.cursor()
	cur.execute("SELECT * FROM commands ORDER BY CASE WHEN type = 'embed' THEN 1 ELSE 2 END DESC, admin ASC, name ASC")
	commands = cur.fetchall()
	cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
	print(cur.fetchall())

	final = []
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
		final.append(obj)

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

def getbans(conn):
	cur = conn.cursor()
	cur.execute("SELECT dcid FROM bans")
	bans = list(cur.fetchall())
	output = []
	for ban in bans:
		output.append(int(ban[0]))
	return output

def addcom(conn, name, content, type, inside, all, admin, keywords, illegals):
	cur = conn.cursor()
	query = "INSERT INTO commands(name,content,type,inside,'all',admin) VALUES ('{}', '{}', '{}', {}, {}, {})".format(name, content, type, int(inside), int(all), int(admin))
	cur.execute(query)
	#conn.commit()
	query = "SELECT id FROM commands WHERE name='{}' AND content='{}' AND type='{}' AND inside={} AND \"all\"={} AND admin={}".format(name, content, type, int(inside), int(all), int(admin))
	cur.execute(query)
	id = cur.fetchall()[0][0]
	for keyword in keywords:
		query = "INSERT INTO keywords(id, keyword) VALUES ({},'{}')".format(id, keyword)
		cur.execute(query)
	for illegal in illegals:
		query = "INSERT INTO illegals(id, illegal) VALUES ({},'{}')".format(id, illegal)
		cur.execute(query)
	conn.commit()

def updatecom(conn, id, name, content, type, inside, all, admin, keywords, illegals):
	cur = conn.cursor()
	query = "UPDATE commands SET name = \"{}\", content = \"{}\", type = \"{}\", inside = {}, 'all' = {}, admin = {} WHERE id = {}".format(name, content, type, int(inside), int(all), int(admin), int(id))
	cur.execute(query)
	query = "DELETE FROM keywords WHERE id={}".format(int(id))
	cur.execute(query)
	for keyword in keywords:
		query = "INSERT INTO keywords(id, keyword) VALUES ({},'{}')".format(id, keyword)
		cur.execute(query)
	query = "DELETE FROM illegals WHERE id={}".format(int(id))
	cur.execute(query)
	for illegal in illegals:
		query = "INSERT INTO illegals(id, illegal) VALUES ({},'{}')".format(id, illegal)
		cur.execute(query)
	conn.commit()

def deletecom(conn, id):
	cur = conn.cursor()
	query = "DELETE FROM commands WHERE id={}".format(int(id))
	cur.execute(query)
	query = "DELETE FROM keywords WHERE id={}".format(int(id))
	cur.execute(query)
	query = "DELETE FROM illegals WHERE id={}".format(int(id))
	cur.execute(query)
	conn.commit()

def addadmin(conn, dcid):
	cur = conn.cursor()
	query = "INSERT INTO admins(dcid) VALUES ({})".format(dcid)
	cur.execute(query)
	conn.commit()

def deleteadmin(conn, dcid):
	cur = conn.cursor()
	query = "DELETE FROM admins WHERE dcid={}".format(dcid)
	cur.execute(query)
	conn.commit()

def addban(conn, dcid):
	cur = conn.cursor()
	query = "INSERT INTO bans(dcid) VALUES ({})".format(dcid)
	cur.execute(query)
	conn.commit()

def deleteban(conn, dcid):
	cur = conn.cursor()
	query = "DELETE FROM bans WHERE dcid={}".format(dcid)
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
