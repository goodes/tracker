#!/usr/bin/env python

import glob
import os
import json
from datetime import datetime
import rethinkdb as r
import pytz
import sys
from beeprint import pp

IL_TZ = pytz.timezone('Israel')

def get_results():
	results = []
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


def get_stats(table, file_path):
	with open(file_path) as src:
		for line in src:
			try:
				data = json.loads(line)
				if 'now_utc' not in data:
					data['now_utc'] = data['now'] + 3600.0*8
				table.insert(data).run()
				sys.stdout.write('.')
			except:
				pass
				sys.stdout.write('#')
			sys.stdout.flush()
if __name__ == "__main__":
	r.connect('rtdb.goodes.net', 28015).repl()
	# # r.db('tracker')
	# res = r.db('tracker').table_drop('items').run()
	# print(json.dumps(res, indent=3, sort_keys=True))
	# res = r.db('tracker').table_create('items').run()
	# print(json.dumps(res, indent=3, sort_keys=True))
	# res = r.db('tracker').table('items').insert(get_results()).run()
	# print(json.dumps(res, indent=3, sort_keys=True))
	get_stats(r.db('customer').table('stats'), sys.argv[1])
