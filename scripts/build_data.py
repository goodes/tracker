#!/usr/bin/env python

import glob
import os
import json
from datetime import datetime
import rethinkdb as r
import pytz

IL_TZ = pytz.timezone('Israel')

state_data = """5808fdf10b910ec9b1246739	https://contestimg.wish.com/api/image/fetch?contest_id=56a9b4982b282a1300eb4459&w=150&h=200	WISH	open
71517977955	https://contestimg.wish.com/api/image/fetch?contest_id=564eb7343a698c4780ad7a34&w=150&h=200	WISH	open
LX207928532CN	https://contestimg.wish.com/api/image/fetch?contest_id=57875cd928d95d089bf36c21&w=150&h=200	WISH	open
RE441164897SE	https://ae01.alicdn.com/kf/HTB1.jBeLXXXXXb6XFXXq6xXFXXXS.jpg_50x50.jpg	Aliexpress	open
RJ890177059CN	https://contestimg.wish.com/api/webimage/57e8d98fc0131112a0ae9b09-0-medium	WISH	open
RK443953098CN	https://ae01.alicdn.com/kf/UT8o8QqXqpaXXagOFbXa.jpg_50x50.jpg	Aliexpress	open
RS220015472CN	https://ae01.alicdn.com/kf/UT877pGXypaXXagOFbXv.jpg_50x50.jpg	Aliexpress	open
RS284979925CN	https://ae01.alicdn.com/kf/UT86YyWXOhXXXagOFbXu.jpg_50x50.jpg	Aliexpress	open
YT1630705114528245	https://contestimg.wish.com/api/image/fetch?contest_id=55bc4ca64d0efc675598d789&w=150&h=200	WISH	open
03702507465	https://ae01.alicdn.com/kf/UT815xjXNRXXXagOFbXC.jpg_50x50.jpg	Aliexpress	delivered
03916503190	https://ae01.alicdn.com/kf/UT8UvaVXUNXXXagOFbXB.jpg_50x50.jpg	Aliexpress	delivered
79337644768184	https://ae01.alicdn.com/kf/UT877pGXypaXXagOFbXv.jpg_50x50.jpg	Aliexpress	delivered
B201607230000851826N	https://contestimg.wish.com/api/image/fetch?contest_id=545dd6843dabbe40f8eec152&w=150&h=200	WISH	delivered
B201608070000916145N	https://contestimg.wish.com/api/image/fetch?contest_id=5684a6a4418eb335f56b7e60&w=150&h=200	WISH	delivered
MP13531322XSG	https://contestimg.wish.com/api/image/fetch?contest_id=54587ce79719cd3fd00f4417&w=150&h=200	WISH	delivered
RI984250225CN	https://img.dxcdn.com/productimages/sku_437478_1_small.jpg	DX	delivered
RJ662519976CN	https://contestimg.wish.com/api/image/fetch?contest_id=57bfdfd7a62ed51f588b15df&w=150&h=200&s=40	WISH	delivered
RS213709730CN	https://contestimg.wish.com/api/image/fetch?contest_id=5613246eb5e28610df5917f7&w=150&h=200	WISH	delivered
RS433270885NL	https://ae01.alicdn.com/kf/UT8J_cUXxdaXXagOFbXh.jpg_50x50.jpg	Aliexpress	delivered
RS628929622NL	https://ae01.alicdn.com/kf/UT8J2hrXMhXXXagOFbXk.jpg_50x50.jpg	Aliexpress	delivered
RS635739575NL	https://www.aliexpress.com/snapshot/8136477786.html?orderId=78600079958184&productId=32604769148	Aliexpress	delivered
WDYK000449697	https://contestimg.wish.com/api/image/fetch?contest_id=564b1542378dcd177386b605&w=150&h=200&s=8	WISH	delivered
YF038327815YW	https://contestimg.wish.com/api/image/fetch?contest_id=567bbc9df05a595e27dc1d9a&w=150&h=200	WISH	delivered
YT1620018979223795	https://contestimg.wish.com/api/image/fetch?contest_id=55b889ab3f6e571f0a047540&w=150&h=200	WISH	delivered
YT1620218979209232	https://contestimg.wish.com/api/image/fetch?contest_id=558e5e954cfec4404b110803&w=150&h=200	WISH	delivered"""

def get_state_data():
	results = {}
	for line in state_data.split('\n'):
		print line
		tracking_id, image_url, vendor, state = line.strip().split('\t')
		results[tracking_id] = dict(image_url=image_url, vendor=vendor, state=state)
	return results

def get_results():
	results = []
	sd = get_state_data()
	for file_path in glob.glob('data/results/*'):
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
		if file_name in sd:
			result.update(sd[file_name])

		results.append(result)
	return results


if __name__ == "__main__":
	sys.exit(1)
	# No more importing for now
	# print(json.dumps(get_state_data(), indent=3, sort_keys=True))
	# r.connect('rtdb.goodes.net', 28015).repl()
	# r.db('tracker')
	# res = r.db('tracker').table_drop('items').run()
	# print(json.dumps(res, indent=3, sort_keys=True))
	# res = r.db('tracker').table_create('items').run()
	# print(json.dumps(res, indent=3, sort_keys=True))
	# res = r.db('tracker').table('items').insert(get_results()).run()
	# print(json.dumps(res, indent=3, sort_keys=True))
