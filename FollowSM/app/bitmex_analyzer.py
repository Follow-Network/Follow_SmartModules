from FollowSM.strategies.bitmex_MACD import Strategy, StrategyMACD, StrategyRSI


class Analyzer:
    def __init__(self, client):
        self.client = client
        self.strategy = None

    def choose_strategy(self, data):
        self.strategy = StrategyMACD(self.client, timeframe='1h')
        print("MACD strategy was chosen")
        # self.strategy = StrategyRSI(self.client, timeframe='1h')
        return self.strategy
