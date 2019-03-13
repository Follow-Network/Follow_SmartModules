# Перенести в отдельный файл с константами
import bitmex
import time
from FollowSM.app.bitmex_trader import Trader


def cycle(trader, time_to_wait_new_trade):
    while True:
        if round(time.time()) % time_to_wait_new_trade == 0:
            print(time.ctime(time.time()))
            print(trader.execute_trade())
            time.sleep(10)


def main():
    client = bitmex.bitmex(
        test=True,  # Use testnet
        api_key="",
        api_secret=""
    )
    time_to_wait_new_trade = 60*30

    trader = Trader(client)
    trader.get_strategy()
    print(trader.get_data())

    print("Decision-making time:", end='')
    print(time.ctime(time.time()))
    # trader.try_order()
    # trader.try_order()
    trader.stoploss()
    # print(trader.execute_trade())

    # cycle(trader, time_to_wait_new_trade)


main()
