#!/usr/bin/env python

import glob
import os
import json
from datetime import datetime
import rethinkdb as r
import pytz

IL_TZ = pytz.timezone('Israel')

def get_results():
	results = []ZZ
	for file_path in glob.glob('../data/results/*'):
		file_name = os.path.split(file_path)[1]
		with open(file_path) as fp:
			result = { 
				'state': 'open',
				'tracking_id': file_name,
				'check_every': 300,
				'status': "".join(fp.readlines()).strip().decode('utf-8'),
				'ts': IL_TZ.localize(datetime.fromtimestamp(os.path.getmtime(file_path))),
				'vendor': '', 
				'expected': IL_TZ.localize(datetime.now())
				}
		# now see if we have an item file, if so, add the data
		item_data_path = os.path.join('data/items', file_name)
		if os.path.exists(item_data_path):
			result.update(json.load(open(item_data_path)))
		results.append(result)
	return results


if __name__ == "__main__":
	r.connect('localhost', 28015).repl()
	r.db('tracker')
	res = r.db('tracker').table_drop('items').run()
	print(json.dumps(res, indent=3, sort_keys=True))
	res = r.db('tracker').table_create('items').run()
	print(json.dumps(res, indent=3, sort_keys=True))
	res = r.db('tracker').table('items').insert(get_results()).run()
	print(json.dumps(res, indent=3, sort_keys=True))