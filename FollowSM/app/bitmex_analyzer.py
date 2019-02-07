from FollowSM.strategies.bitmex_MACD import Strategy


class Analyzer:
    def __init__(self, client):
        self.client = client
        self.strategy = None

    def choose_strategy(self):
        self.strategy = Strategy(self.client, timeframe='1h')
        print("MACD strategy was chosen")
        return self.strategy
