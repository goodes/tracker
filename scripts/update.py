#!/usr/bin/env python

import glob
import os
import json
from datetime import datetime
import rethinkdb as r
import pytz
from pprint import pprint as pp
#from beeprint import pp
import requests
import slack
from bs4 import BeautifulSoup

#POSTIL_URL = "http://www.israelpost.co.il/itemtrace.nsf/trackandtraceJSON?OpenAgent&lang=EN&itemcode={}"
POSTIL_URL = "http://www.israelpost.co.il/itemtrace.nsf/trackandtraceJSON?openagent&lang=EN&itemcode={}"
IL_TZ = pytz.timezone('Israel')
RTDB_SERVER = os.getenv('RTDB_SERVER', 'rtdb.goodes.net')
TECHNICAL_ISSUES = 'Sorry! Due to a technical problem, this service is unavailable at the moment'

def setup():
	r.connect(RTDB_SERVER, 28015).repl()
	db = r.db('tracker')

	try:
		if 'log' not in db.table_list().run():
			db.table_create('log').run()
	except Exception as ex:
		print str(ex)

def update():
    r.connect(RTDB_SERVER, 28015).repl()
    db = r.db('tracker')
    res = db.table('items')
    for item in res.filter({'state': 'open'}).run():
        if len(item['tracking_id']) > 0:  # and item['tracking_id'][0].isalpha():
            status, result = get_status(item['tracking_id'])
            # print item['tracking_id'], str(status), str(result.encode('utf-8'))
            if status in ['ERROR', 'GOOD']:
                if item['status'] != result:
                    if not result.encode('utf-8').startswith(TECHNICAL_ISSUES):
                        now = IL_TZ.localize(datetime.now())
                        log(db, item['id'], item['ts'], now, item['status'], result)
                        update = {'id': item['id'], 'ts': now, 'status': result}
                        pp(update)
                        res.update(update).run()
                        message = u"TRACKER: *{}*  ({})\n*{}*\nNow:\n{}".format(
                            item['tracking_id'],
                            item['vendor'],
                            item['title'],
                            result).encode('utf-8')
                        print message
                        slack.post(message)
		else:
		    print "IGNORE", item['tracking_id']

def log(db, item_id, last_ts, current_ts, was, now):
	entry = {
		'item_id': item_id,
		'last_ts': last_ts,
		'current_ts': current_ts,
		'was': was,
		'now': now,
        'seen': False,
	}

	pp(entry)
	db.table('log').insert(entry).run()

def get_status(tracking_id):
	url = POSTIL_URL.format(tracking_id)
	try:
		resp = requests.get(url)
		resp.raise_for_status()
		data = resp.json()
		return process_response(data)
	except:
		return "BAD", url

def process_response(data):
    # print "\n" + "-"*80 + "\n" + tracking_id
    # print json.dumps(data, indent=3, sort_keys=True)
	if data['data_type'].startswith('ERROR'):
		return "ERROR", data['itemcodeinfo'].split('<br>')[0]
	else:
                if data['itemcodeinfo'].startswith('<table'):
                    soup = BeautifulSoup(data['itemcodeinfo'], 'html.parser')
                    return "GOOD", soup.find_all('tr')[1].find_all('td')[-1].text
                else:
                    return "GOOD", data['itemcodeinfo'].split('<br>')[0]


if __name__ == "__main__":
	setup()
	update()
