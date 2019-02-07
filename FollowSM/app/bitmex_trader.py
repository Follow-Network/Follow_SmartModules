# Can open and close orders using prediction from the Strategy class
from FollowSM.app.bitmex_analyzer import Analyzer


class Trader:
    def __init__(self, client, strategy_stoploss="", money_to_trade=100, leverage=5, pair="XBTUSD"):
        # Client is a bitmex object with user's keys
        self.client = client
        self.strategy = None
        self.money_to_trade = money_to_trade
        self.leverage = leverage
        self.pair = pair
        self.strategy_stoploss = strategy_stoploss

    # Check all open orders on the account
    def get_data(self):
        result = self.client.OrderBook.OrderBook_getL2(symbol=self.pair).result()
        print(result)
        return 1

    def get_strategy(self):
        analyzer = Analyzer(self.client)
        self.strategy = analyzer.choose_strategy()

    # Get list of all pairs on the exchange
    def check_pairs(self):
        pass

    # Check the stoploss indicator
    def stoploss(self):
        pass

    # Open/close orders
    def execute_trade(self):
        prediction = self.strategy.predict()
        print("Last prediction:", prediction)
        try:
            if prediction == -1:
                response = self.client.Order.Order_new(
                    symbol=self.pair,
                    side="Sell",
                    orderQty=self.money_to_trade * self.leverage,
                ).result()
                print("Sell order was created:\npair:", self.pair, "\namount:", self.money_to_trade * self.leverage)
            if prediction == 1:
                response = self.client.Order.Order_new(
                    symbol=self.pair,
                    side="Buy",
                    orderQty=self.money_to_trade * self.leverage,
                ).result()
                print("Buy order was created:\npair:", self.pair, "\namount:", self.money_to_trade * self.leverage)
        except Exception as e:
            print("Error")
            print(str(e))
        return True
