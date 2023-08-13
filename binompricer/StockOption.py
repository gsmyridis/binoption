from .Stock import Stock


class StockOption(Stock):
    """
    Stores common attributes of a stock option
    """

    def __init__(self, strike, maturity,
                 initial_price=None, price_tree=None, steps=2,
                 probs=(None, None), price_changes=(None, None), tree_method='multiply',
                 int_rate=0.05, int_rates_tree=None, volatility=0, dividents=0,
                 is_put=False, is_american=False):
        super().__init__(initial_price, price_tree, maturity, steps, probs, price_changes, tree_method,
                         int_rate, int_rates_tree, volatility, dividents)
        """
        Initialize the stock option class
        Defaults to European call unless specified
        :param strike: strike price
        :param maturity: time to maturity
        :param is_put: True for a put option,
                       False for a call option
        :param is_american: True for an American option,
                            False for a European option
                            
        :attr hedge_ratios: hedge ratios at every step
        """
        self.strike = strike
        self.maturity = maturity
        self.is_call = not is_put
        self.is_european = not is_american
