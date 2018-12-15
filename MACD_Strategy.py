import numpy
import talib
import requests
import json
import time

from datetime import datetime

BEAR_PERC = 70
BULL_PERC = 30

PAIR = 'BTC_ETH'

def should_buy(pair):
    
    start_time = time.time() - 15*60*60
    resource = requests.get("https://poloniex.com/public?command=returnChartData&currencyPair=%s&start=%s&end=9999999999&period=300" % (pair, start_time))
    data = json.loads(resource.text)

    quotes = {}
    quotes['close']=numpy.asarray([item['close'] for item in data])
    macd, macdsignal, macdhist = talib.MACD(quotes['close'], fastperiod=12, slowperiod=26, signalperiod=9)

    idx = numpy.argwhere(numpy.diff(numpy.sign(macd - macdsignal)) != 0).reshape(-1) + 0

    inters = []

    for offset, elem in enumerate(macd):
        if offset in idx:
            inters.append(elem)
        else:
            inters.append(numpy.nan)

    hist_data = []
    max_v = 0

    for offset, elem in enumerate(macdhist):
        activity_time = False
        curr_v = macd[offset] - macdsignal[offset]
        if abs(curr_v) > abs(max_v):
            max_v = curr_v
        perc = curr_v/max_v
        
        if       (   (macd[offset] > macdsignal[offset] and perc*100 > BULL_PERC) # восходящий тренд
                     or      (
                                 macd[offset] < macdsignal[offset] and perc*100 < (100-BEAR_PERC)
                            )

                ):
            v = 1
            activity_time = True
        else:
            v = 0
            
        if offset in idx and not numpy.isnan(elem):
            # тренд изменился
            max_v = curr_v = 0 # обнуляем пик спреда между линиями
        hist_data.append(v*1000)
 
    return activity_time

while True:
    print("Покупать?", should_buy(PAIR))
    time.sleep(1)