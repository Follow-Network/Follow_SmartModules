import numpy
import talib
import requests
import json
import time

from datetime import datetime

BEAR_PERC = 70
BULL_PERC = 30

PAIR = 'BTC_USD'

def should_buy(pair):

	resource = requests.get('https://api.exmo.com/v1/trades/?pair=%s&limit=10000' % pair)
	data = json.loads(resource.text)

	close_prices = {}
	for item in reversed(data[pair]):
		d = int(float(item['date'])/300)*300
		close_prices[d] = float(item['price'])

	macd, macdsignal, macdhist = talib.MACD(numpy.asarray([close_prices[item] for item in sorted(close_prices)]), fastperiod=12, slowperiod=26, signalperiod=9)

	idx = numpy.argwhere(numpy.diff(numpy.sign(macd - macdsignal)) != 0).reshape(-1) + 0

	inters=[]

	for offset, elem in enumerate(macd):
		if offset in idx:
			inters.append(elem)
		else:
			inters.append(numpy.nan)

	hist_data = []
	max_v = 0

	activity_time = False
	for offset, elem in enumerate(macdhist):
		activity_time = False
		curr_v = macd[offset]-macdsignal[offset]
		if abs(curr_v) > abs(max_v):
			max_v = curr_v
		perc = curr_v/max_v

		if 		(	(macd[offset] > macdsignal[offset] and perc*100 > BULL_PERC)
					or (
						macd[offset] < macdsignal[offset] and perc*100 < (100-BEAR_PERC)
						)
				):
			v = 1
			activity_time = True
		else:
			v = 0

		if offset in idx and not numpy.isnan(elem):
			max_v = curr_v = 0
		hist_data.append(v*1000)

	return activity_time

while True:
	print("Покупать?", should_buy(PAIR))
	time.sleep(1)