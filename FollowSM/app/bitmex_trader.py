# Can open and close orders using prediction from the Strategy class
class Trader:
    def __init__(self, client, strategy, money_to_trade=100, leverage=5, pair="XBTUSD"):
        # Client is a bitmex object with user's keys
        self.client = client
        self.strategy = strategy
        self.money_to_trade = money_to_trade
        self.leverage = leverage
        self.pair = pair

    # Check all open orders on the account
    def check_orders(self):
        result = self.client.OrderBook.OrderBook_getL2(symbol=self.pair).result()
        print(result)
        return 1

    # Get list of all pairs on the exchange
    def check_pairs(self):
        pass

    # Check the stoploss indicator
    def stoploss(self, strategy_stoploss):
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
            if prediction == 1:
                response = self.client.Order.Order_new(
                    symbol=self.pair,
                    side="Buy",
                    orderQty=self.money_to_trade * self.leverage,
                ).result()
        except Exception as e:
            print("Error")
            print(str(e))
        return True
