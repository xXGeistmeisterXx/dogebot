from flask import Flask, request
from threading import Thread
import os
import sys
from queue import Queue
import _thread
import subprocess
import time
import json
import requests

def log(content):
	f = open("log.txt", "a")
	now = time.strftime('%H:%M %m/%d/%Y')
	content = "[%s] %s\n" % (now, content)
	f.write(content)
	f.close()

app = Flask('')

@app.route('/')
def home():
	return "I'm alive"

@app.route('/ping')
def ping():
	log("IFTTT PING")
	return "ping"

@app.route('/status', methods=['GET', 'POST'])
def status():
	global status
	if request.method == 'GET':
		log("IFTTT GET STATUS")
	else:
		log("IFTTT GET STATUS (AUTO)")
	sstatus = "ONLINE" if status else "OFFLINE"
	obj = {"value1" : sstatus}
	purl = "https://maker.ifttt.com/trigger/status/with/key/df9JDzUJhVJ52dsn5HxnUpcwOvhRWIoPJ4kY2YC3RQT"
	r = requests.post(purl, json = obj)
	return "yes"

@app.route('/data')
def send():
	global status
	global key
	global m
	auth = request.args.get('token')
	data = request.args.get('data')
	prot = request.args.get('protocol')
	data = data[1:]
	prot = int(prot)
	if key == auth:
		if prot == 1:
			if data == "restart":
				#log("RESTARTED BY IFTTT")
				pass
			elif data == "stop":
				#log("STOPPED BY IFTTT")
				pass
			elif data == "start":
				#log("STARTED BY IFTTT")
				pass
		elif prot == 400:
			ldata = data.split()
			q.put(["find", " ".join(ldata[2:]), ldata[0], ldata[1]])
		elif prot == 401:
			#fake-general, RDS
			q.put(["pre", data, 648371226930184226])
		elif prot == 402:
			#dogebot-testing, RDS
			q.put(["pre", data, 655834103048044554])
		elif prot == 403:
			#general, DVS
			q.put(["pre", data, 693229884352233543])
	return "yes"


def run():
  app.run(host='0.0.0.0',port=5555)

def keep_alive(u):
	global key
	global q
	global status
	q = u
	t = Thread(target=run)
	key = os.environ.get("AUTH")
	status = True
	t.start()
