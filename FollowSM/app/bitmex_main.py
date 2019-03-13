# Перенести в отдельный файл с константами
import bitmex
import time
from FollowSM.app.bitmex_trader import Trader
from FollowSM.strategies.bitmex_MACD import Strategy

client = bitmex.bitmex(
    test=True,  # Use testnet
    api_key="",
    api_secret=""
)
time_to_wait_new_trade = 60*60
strategy = Strategy(client, timeframe='1h')
trader = Trader(client, strategy)
print(trader.check_orders())

# print("Decision-making time:")
# print(time.ctime(time.time()))
# print(trader.execute_trade())

# while True:
#     if round(time.time()) % time_to_wait_new_trade == 0:
#         print(trader.execute_trade())
#         print(time.ctime(time.time()))
#         time.sleep(10)
