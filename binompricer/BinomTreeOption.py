from .StockOption import StockOption
import numpy as np


class BinomialTreeOption(StockOption):
    """
    Price a European or American option by the binomial tree
    """

    def __init__(self, strike, maturity, initial_price=None, price_tree=None, steps=2,
                 probs=(None, None), price_changes=(None, None), tree_method='multiply',
                 int_rate=0.05, int_rates_tree=None, volatility=0, dividents=0,
                 is_put=False, is_american=False):
        super().__init__(strike, maturity, initial_price, price_tree, steps, probs, price_changes, tree_method,
                         int_rate, int_rates_tree, volatility, dividents, is_put, is_american)

        """
        Set up the parameters that are needed for the model
        """
        self.hedge_ratios = []
        self.payoff_tree = []
        self.premium = 0

    def init_payoffs_tree(self):
        """
        Returns the payoffs for the option at each time step
        """
        if self.is_call:
            return np.maximum(0, self.price_tree[self.steps] - self.strike)
        else:
            return np.maximum(0, self.strike - self.price_tree[self.steps])

    def check_early_exercise(self, payoffs, node):
        """
        Check if it's worth exercising now
        """
        if self.is_call:
            return np.maximum(payoffs, self.price_tree[node] - self.strike)
        else:
            return np.maximum(payoffs, self.strike - self.price_tree[node])

    def traverse_tree(self):
        """
        Starting from the time of maturity, traverse backwards
        and calculate discounted payoffs at each node
        """
        payoffs = self.init_payoffs_tree()
        self.payoff_tree = [payoffs]
        for i in reversed(range(self.steps)):
            # The payoffs from not exercising the option
            payoffs = (self.discounts[i] * (payoffs[:-1] * self.risk_free_probs_up[i]
                                            + payoffs[1:] * self.risk_free_probs_down[i]))
            # Payoffs from exercising, for American options
            if not self.is_european:
                payoffs = self.check_early_exercise(payoffs, i)
            self.payoff_tree.append(payoffs)

        self.payoff_tree = self.payoff_tree[::-1]
        return self.payoff_tree

    def price(self):
        """
        Entry point of the pricing implementation
        """
        self.calc_price_tree()
        self.calc_interest_factors()
        self.calc_risk_neutral_probs()
        payoffs = self.traverse_tree()
        # Option value at time 0 converges to first node
        self.premium = payoffs[0].item()

        return self.premium

    def calc_hedge_ratios(self):
        """
        Calculates the hedge ratios as every node of the tree
        """
        for i in range(1, len(self.payoff_tree)):
            dw = self.payoff_tree[i][1:] - self.payoff_tree[i][:-1]
            ds = self.price_tree[i][1:] - self.price_tree[i][:-1]
            self.hedge_ratios.append(np.divide(dw, ds))

        return self.hedge_ratios
