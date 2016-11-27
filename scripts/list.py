#!/usr/bin/env python
from datetime import datetime
import rethinkdb as r
from beeprint import pp


r.connect('rtdb.goodes.net', 28015).repl()
db = r.db('tracker')
for item in db.table('log').order_by('current_ts').eq_join('item_id', db.table('items')).run():
    print "{:30} {:40}".format(item['left']['last_ts'].ctime(), item['right']['tracking_id'])
    print "{:30} {}".format('', item['right']['title'])
    print "{:30} {}".format('', item['left']['now'])
    # pp(item)
