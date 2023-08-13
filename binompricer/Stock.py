import numpy as np
import math


class Stock(object):
    """
    Stores commont attributtes of stocks and interest rates
    """

    def __init__(self, initial_price=None, price_tree=None, maturity=1, steps=2,
                 probs=(None, None), price_changes=(None, None), tree_method='multiply',
                 int_rate=0.05, int_rates_tree=None, volatility=0, dividents=0):
        """
        Stores common attributes for a stock futures contract
        :param initial_price: value of the stock at time t=0
        :param price_tree: stock price tree
        :param maturity: maturity time
        :param steps: steps for the pricing
        :param probs: [probability to the up-state, probability to the down-state]
        :param price_changes: [price change to the up-state, price change to the down-state]
        :param tree_method: Method with which we construct the price tree
                'multiply': for price_changes to be factors
                'add': for price_changes to be summands
        :param int_rate: risk-free interest rate
        :param int_rates_tree: interest rates tree
        :param volatility: volatility
        :param dividents: divident yield
        """

        self.maturity = maturity
        self.pu, self.pd = probs[0], probs[1]
        self.u, self.d = price_changes[0], price_changes[1]
        self.steps = steps
        self.initial_price = initial_price
        self.price_tree = price_tree
        self.tree_method = tree_method

        self.volatility = volatility
        self.dividents = dividents

        if price_tree is None:
            cond1 = (self.pu is None and self.pd is None) and (self.u is None or self.d is None)
            cond2 = (self.pu is None or self.pd is None) and (self.u is None and self.d is None)
            if initial_price is None or cond1 or cond2 or self.steps is None:
                raise ValueError("If no stock 'price_tree' is provided, then 'initial_price' and 'steps' "
                                 "must be specified, along with 'probs' or 'price_changes'.")
            self.probs_are_set = self.pu is not None and self.pd is not None
            self.price_changes_are_set = self.u is not None and self.d is not None
            if self.probs_are_set and self.price_changes_are_set:
                raise ValueError("You can specify either 'probs' or 'price_changes', not both.")

            # Check for non-zero probs or price_changes
            if (not self.price_changes_are_set) and self.pu == 0 and self.pd == 0:
                raise ValueError("When you specify probs, they cannot both be zero.")
            if (not self.probs_are_set) and self.u == 0 and self.d == 0:
                raise ValueError("When you specify price_changes, they cannot be both zero.")

            if not self.price_changes_are_set:
                self.u = 1 + self.pu
                self.d = 1 - self.pd

        else:
            self.tree_method = 'direct'

        self.dt = self.maturity / float(self.steps)
        self.int_rate = int_rate
        self.interest_factors = []
        self.int_rates_tree = int_rates_tree
        self.discounts = []
        self.risk_free_probs_up = []
        self.risk_free_probs_down = []

    @property
    def maturity(self):
        """ Getter for maturity time """
        return self._maturity

    @maturity.setter
    def maturity(self, maturity):
        """ Setter for maturity time """
        if maturity <= 0:
            raise ValueError("Maturity time has to be larger than zero.")
        self._maturity = maturity

    @property
    def pu(self):
        """ Getter of probability to the up-state """
        return self._pu

    @pu.setter
    def pu(self, pu):
        """ Setter of probability to the up-state """
        if pu is not None and (pu < 0 or pu > 1):
            raise ValueError("Probabilities have to lie in the range from 0 to 1.")
        else:
            self._pu = pu

    @property
    def pd(self):
        """ Getter of probability to the down-state """
        return self._pd

    @pd.setter
    def pd(self, pd):
        """ Setter of probability to the down-state """
        if pd is not None and (pd < 0 or pd > 1):
            raise ValueError("Probabilities have to lie in the range from 0 to 1.")
        else:
            self._pd = pd

    @property
    def u(self):
        """ Getter for price change to the upstate """
        return self._u

    @u.setter
    def u(self, u):
        """ Setter for the price change to the up-state """
        if u is not None and u < 0:
            raise ValueError("Factors and summands have to be non-negative.")
        else:
            self._u = u

    @property
    def d(self):
        """ Getter for the price change to the down-state """
        return self._d

    @d.setter
    def d(self, d):
        """ Setter for the price change to the down-state """
        if d is not None and d < 0:
            raise ValueError("Factors and summands have to be non-negative.")
        else:
            self._d = d

    @property
    def price_tree(self):
        """ Price tree getter """
        return self._price_tree

    @price_tree.setter
    def price_tree(self, price_tree):
        """ Sets the price tree """
        if price_tree is not None:
            if not price_tree:
                raise ValueError("The price tree cannot be of zero length.")
            else:
                for i, array in enumerate(price_tree):
                    if len(array) != i + 1:
                        raise ValueError("Assuming the tree is recombining, the number of nodes should start from one"
                                         " and increase by one.")
                self.steps = len(price_tree) - 1
                self.initial_price = price_tree[0][0]
                self._price_tree = [np.array(lst) for lst in price_tree]
        else:
            self._price_tree = None

    @property
    def tree_method(self):
        """ Tree method getter """
        return self._tree_method

    @tree_method.setter
    def tree_method(self, tree_method):
        """ Sets tree method """
        if tree_method not in ['multiply', 'add', 'direct']:
            raise ValueError("Tree_method can only be 'multiply', 'add' or 'direct'.")
        if tree_method == 'direct' and self.price_tree is None:
            raise ValueError("Your tree_method is 'direct', but you have not provided a price_tree.")

        self._tree_method = tree_method

    def calc_price_tree(self):
        """
        Calculates the stock price tree using the factors or summands u and d.
        """
        if self.price_tree is None:
            # Initialize a 2D tree at t=0
            price_tree = [np.array([self.initial_price])]
            # Simulate all possible stock prices path
            for i in range(self.steps):
                prev_branches = price_tree[-1]

                if self.tree_method == 'multiply':
                    st = np.concatenate(
                        (prev_branches * self.u,
                         [prev_branches[-1] * self.d]))
                elif self.tree_method == 'add':
                    st = np.concatenate(
                        (prev_branches + self.u,
                         [prev_branches[-1] - self.d]))

                # Add nodes at each time step
                price_tree.append(st)
            self.price_tree = price_tree

    @property
    def int_rates_tree(self):
        """ Getter of interest rates tree """
        return self._int_rates_tree

    @int_rates_tree.setter
    def int_rates_tree(self, int_rates_tree):
        """
        Setter of interest rates tree
        Every time the interes rates tree is set,
        the discounting tree is also calculated
         """
        if int_rates_tree is None:
            if self.int_rate is None:
                raise ValueError("If no 'int_rates_tree' is provided, 'int_rate' has to be specified.")
            self._int_rates_tree = int_rates_tree
        else:
            for i, array in enumerate(int_rates_tree):
                if len(array) != i + 1:
                    raise ValueError("Assuming the tree is recombining, the number of nodes should start from one"
                                     " and increase by one.")
            if len(int_rates_tree) < self.steps:
                raise ValueError("The 'int_rates_tree' must have length at least equal to 'steps' - 1.")

            self._int_rates_tree = [np.array(lst) for lst in int_rates_tree]

    def calc_interest_factors(self):
        """ Calculates discounting tree """
        if self.int_rates_tree is None:
            dr = math.exp((self.int_rate - self.dividents) * self.dt)  # Interest factor for each step
            self.interest_factors = []
            self.discounts = []
            for i in range(1, self.steps + 1):
                self.interest_factors.append(np.full(i, dr))
                self.discounts.append(np.full(i, 1 / dr))
        else:
            self.interest_factors = [np.array([math.exp((rtj - self.dividents) * self.dt) for rtj in rt])
                                     for rt in self.int_rates_tree]
            self.discounts = [np.array([1 / dr_nj for dr_nj in dr_n])
                              for dr_n in self.interest_factors]

    def calc_risk_neutral_probs(self):
        """
        Calculates the risk-neutral probabilities tree
        """
        rf_probs_up = []
        for n in range(self.steps):
            numerator = self.price_tree[n][:] * self.interest_factors[n][:] - self.price_tree[n+1][1:]
            denominator = self.price_tree[n+1][:-1] - self.price_tree[n+1][1:]
            rf_probs_up.append(np.array(numerator / denominator))
        self.risk_free_probs_up = np.array(rf_probs_up, dtype=object)
        self.risk_free_probs_down = 1 - self.risk_free_probs_up
