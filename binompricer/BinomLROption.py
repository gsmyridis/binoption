import math
from .BinomTreeOption import BinomialTreeOption


class BinomialLROption(BinomialTreeOption):

    """
    Price an option with the Leisen - Reimer tree
    """

    def __init__(self, strike, maturity, initial_price, price_tree=None, steps=2,
                 probs=(0.5, 0.5), price_changes=(None, None), tree_method='multiply',
                 int_rate=0.05, int_rates_tree=None, volatility=0, dividents=0,
                 is_put=False, is_american=False):
        super().__init__(strike, maturity, initial_price, price_tree, steps, probs, price_changes, tree_method,
                         int_rate, int_rates_tree, volatility, dividents, is_put, is_american)
        """
        Set up the parameters that are needed for the model

        :attr u: Expected value in the up state
        :attr d: Expected value in the down state
        :attr qu: Risk-free probability to the upstate
        :attr qd: Risk-free probability to the downstate
        """

        odd_steps = self.steps if (self.steps % 1 == 0) else (self.steps + 1)
        df = math.exp(-(self.int_rate - self.dividents) * self.dt)

        term_1 = math.log(self.initial_price / self.strike)
        term_21 = (self.int_rate - self.dividents) * self.maturity
        term_22 = (self.volatility ** 2 / 2) * self.maturity
        term_3 = self.volatility * math.sqrt(self.maturity)

        d1 = (term_1 + term_21 + term_22) / term_3
        d2 = (term_1 + term_21 - term_22) / term_3

        pbar = self.pp_inversion(d1, odd_steps)
        self.p = self.pp_inversion(d2, odd_steps)
        self.u = 1 / df * pbar / self.p
        self.d = (1 / df - self.p * self.u) / (1 - self.p)
        self.qu = self.p
        self.qd = 1 - self.p

    @staticmethod
    def pp_inversion(z, n):
        """
        Peizer and Pratt inversion formula
        """
        exponent = - (z / (n + 1/3 + 0.1 / (n + 1))) ** 2 * (n + 1/6)
        return 0.5 + math.copysign(1, z) * math.sqrt(0.25 - 0.25 * math.exp(exponent))
