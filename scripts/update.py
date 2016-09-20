#!/usr/bin/env python

import glob
import os
import json
from datetime import datetime
import rethinkdb as r
import pytz
from beeprint import pp
import requests

POSTIL_URL = "http://www.israelpost.co.il/itemtrace.nsf/trackandtraceJSON?OpenAgent&lang=EN&itemcode={}"
IL_TZ = pytz.timezone('Israel')

def update():
	r.connect('localhost', 28015).repl()
	db = r.db('tracker')
	res = db.table('items')
	for item in res.filter({'state': 'open'}).run():
		if len(item['tracking_id']) > 0:  # and item['tracking_id'][0].isalpha():
			status, result = get_status(item['tracking_id'])
			if status in ['ERROR', 'GOOD']:
				if item['status'] != result:
					now = IL_TZ.localize(datetime.now())
					log(db, item['id'], item['ts'], now, item['status'], result)
					update = {
						'id': item['id'],
						'ts': now,
						'status': result,
						}
					pp(update)
					res.update(update).run()
					# print "WAS: {}\nNOW: {}".format(item['status'], result)
		else:
			print "IGNORE", item['tracking_id']

def log(db, item_id, last_ts, current_ts, was, now):
	entry = {
		'item_id': item_id,
		'last_ts': last_ts,
		'current_ts': current_ts,
		'was': was,
		'now': now
	}
	pp(entry)
	db.table('log').insert(entry).run()

def get_status(tracking_id):
	url = POSTIL_URL.format(tracking_id)
	try:
		resp = requests.get(url)
		resp.raise_for_status()
		data = resp.json()
		if data['data_type'].startswith('ERROR'):
			return "ERROR", data['itemcodeinfo'].split('<br>')[0]
		else:
			return "GOOD", data['itemcodeinfo'].split('<br>')[0]
	except:
		return "BAD", url
	
if __name__ == "__main__":
	update()