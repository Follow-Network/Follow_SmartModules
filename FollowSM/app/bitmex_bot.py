# transfer Trader class into another file
import bitmex
import talib
import pandas as pd

# Main bot class
# Can open and close orders using prediction from the Strategy class
class Trader:
    def __init__(self, client, strategy, money_to_trade=100, leverage=5):
        # Client is a bitmex object with user's keys
        self.client = client
        self.strategy = strategy
        self.money_to_trade = money_to_trade
        self.leverage = leverage

    def execute_trade(self):
        prediction = self.strategy.predict()
        print("Last prediction:", prediction)
        try:
            if prediction == -1:
                response = self.client.Order.Order_new(
                    symbol="XBTUSD",
                    side="Sell",
                    orderQty=self.money_to_trade * self.leverage,
                ).result()
            if prediction == 1:
                response = self.client.Order.Order_new(
                    symbol="XBTUSD",
                    side="Buy",
                    orderQty=self.money_to_trade * self.leverage,
                ).result()
        except Exception as e:
            print("Error")
            print(str(e))
        return True

# Uses macd from talib library
class Strategy:
    def __init__(self, client, timeframe='5m'):
        self.client = client
        self.timeframe = timeframe

    # Makes a prediction:
    # "1" to bye
    # "-1" to sell
    # "0" to ignore
    def predict(self):
        # Getting {count} candles/timeframe
        ohlcv_candles = pd.DataFrame(self.client.Trade.Trade_getBucketed(
            binSize=self.timeframe,
            symbol='XBTUSD',
            count=100,
            reverse=True
        ).result()[0])
        ohlcv_candles.set_index(['timestamp'], inplace=True)
        # fastperiod=8, slowperiod=28, signalperiod=9
        macd, signal, hist = talib.MACD(ohlcv_candles.close.values, fastperiod=0, slowperiod=0, signalperiod=0)
        # Sell
        if hist[-1] < 0 < hist[-2]:
            return -1
        # Buy
        elif hist[-1] > 0 > hist[-2]:
            return 1
        # Not clear, goto next
        else:
            return 0


client = bitmex.bitmex(
    test=True,
    api_key="vPa4Ae_LsMnoZVwCH0784wIV",
    api_secret="KBcPfBBQa3WeU5sNe3SM197iys9kL8J2z82XFRihdSEE92xZ"
)

strategy = Strategy(client, timeframe='1h')
trader = Trader(client, strategy)

print(trader.execute_trade())
