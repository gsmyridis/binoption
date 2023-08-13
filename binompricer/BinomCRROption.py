from .BinomTreeOption import BinomialTreeOption
import math


class BinomialCRROption(BinomialTreeOption):
    """
    Price an option with the binomial CRR model
    """
    def __init__(self, strike, maturity, initial_price, price_tree=None, steps=2,
                 probs=(0.5, 0.5), price_changes=(None, None), tree_method='multiply',
                 int_rate=0.05, int_rates_tree=None, volatility=0.3, dividents=0,
                 is_put=False, is_american=False):
        super().__init__(strike, maturity, initial_price, price_tree, steps, probs, price_changes, tree_method,
                         int_rate, int_rates_tree, volatility, dividents, is_put, is_american)
        """
        Set up the parameters that are needed for the model

        :attr u: Expected value in the up state
        :attr d: Expected value in the down state
        :attr R: Interest factor (1 + int_rate * dt)
        :attr qu: Risk-free probability to the upstate
        :attr qd: Risk-free probability to the downstate
        """

        self.u = math.exp(self.volatility * math.sqrt(self.dt))
        self.d = 1 / self.u
