from .Stock import Stock


class StockFutures(Stock):

    def __init__(self, initial_price=None, price_tree=None, maturity=1, steps=2,
                 probs=(0.5, 0.5), price_changes=(None, None), tree_method='multiply',
                 int_rate=0.05, int_rates_tree=None, volatility=0, dividents=0):
        super().__init__(initial_price, price_tree, maturity, steps,
                         probs, price_changes, tree_method,
                         int_rate, int_rates_tree, volatility, dividents)
        """
        Stores common attributes for a stock futures contract
        """




