import talib
import pandas as pd


class Strategy:
    def predict(self) -> int:
        raise NotImplementedError


# Uses macd from talib library
class StrategyMACD(Strategy):
    def __init__(self, client, timeframe='1h'):
        self.client = client
        self.timeframe = timeframe

    # Makes a prediction:
    # "1" to bye
    # "-1" to sell
    # "0" to ignore
    def predict(self) -> int:
        # Getting {count} candles during timeframe and creating a dataframe
        ohlcv_candles = pd.DataFrame(self.client.Trade.Trade_getBucketed(
            binSize=self.timeframe,
            symbol='XBTUSD',
            count=100,
            reverse=True
        ).result()[0])
        ohlcv_candles.set_index(['timestamp'], inplace=True)
        # fastperiod=8, slowperiod=28, signalperiod=9
        macd, signal, hist = talib.MACD(ohlcv_candles.close.values, fastperiod=8, slowperiod=28, signalperiod=9)
        # Sell
        if hist[-1] < 0 < hist[-2]:
            return -1
        # Buy
        elif hist[-1] > 0 > hist[-2]:
            return 1
        # Not clear, goto next
        else:
            return 0