from .StockFutures import StockFutures
from .Stock import Stock


class BinomialTreeFutures(StockFutures):
    """
    Prices a stock futures contract

    """
    def __init__(self, initial_price=None, price_tree=None, maturity=1, steps=2,
                 probs=(0.5, 0.5), price_changes=(None, None), tree_method='multiply',
                 int_rate=0.05, int_rates_tree=None, volatility=0, dividents=0):
        super().__init__(initial_price, price_tree, maturity, steps,
                         probs, price_changes, tree_method,
                         int_rate, int_rates_tree, volatility, dividents)
        """
        Set up the parameters that are needed for the model

        :attr num_term_nodes: Number of terminal nodes in the tree
        :attr u: Expected value in the up state
        :attr d: Expected value in the down state
        :attr R: Interest factor (1 + int_rate * dt)
        :attr qu: Risk-free probability to the upstate
        :attr qd: Risk-free probability to the downstate
        """
        self.hedge_ratios = []
        self.premium = 0
        self.futures_tree = []

    def init_futures_tree(self):
        """
        Initiates futures tree
        """
        return self.price_tree[-1]

    def traverse_tree(self, futures_prices):
        """
        Traverses binomial tree
        """
        self.futures_tree = [futures_prices]
        for n in reversed(range(self.steps)):
            # Backwards formula
            futures_prices = (self.risk_free_probs_up[n] * futures_prices[:-1]
                              + self.risk_free_probs_down[n] * futures_prices[1:])
            self.futures_tree.append(futures_prices)

    def price(self):
        """
        Entry point of the pricing implementation
        """
        self.calc_price_tree()
        self.calc_interest_factors()
        self.calc_risk_neutral_probs()
        futures_prices = self.init_futures_tree()
        self.traverse_tree(futures_prices)
        self.premium = self.futures_tree[-1].item()

        return self.premium
