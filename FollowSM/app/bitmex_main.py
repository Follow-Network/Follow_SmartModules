# Перенести в отдельный файл с константами
import bitmex
import time
from FollowSM.app.bitmex_trader import Trader


def main():
    client = bitmex.bitmex(
        test=True,  # Use testnet
        api_key="vPa4Ae_LsMnoZVwCH0784wIV",
        api_secret="KBcPfBBQa3WeU5sNe3SM197iys9kL8J2z82XFRihdSEE92xZ"
    )
    time_to_wait_new_trade = 60*30

    trader = Trader(client)
    trader.get_strategy()
    # print(trader.get_data())

    print("Decision-making time:")
    print(time.ctime(time.time()))
    print(trader.execute_trade())

    while True:
        if round(time.time()) % time_to_wait_new_trade == 0:
            print(time.ctime(time.time()))
            print(trader.execute_trade())
            time.sleep(10)


main()
