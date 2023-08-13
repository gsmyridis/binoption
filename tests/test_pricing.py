import unittest
import sys
import os
import utils
import numpy as np
# Get the path to the parent directory (project directory)
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the project directory to the Python path
sys.path.insert(0, project_dir)

from binompricer import BinomialTreeOption
from binompricer import BinomialCRROption
from binompricer import BinomialLROption
from binompricer import BinomialTreeFutures


class BinomialTreeTest(unittest.TestCase):
    """
    Pricing tests for options
    """
    def test_european_put(self):
        """
        Test for European put option
        """
        eu_put_option = BinomialTreeOption(initial_price=50, strike=52, int_rate=0.05, maturity=2,
                                           steps=2, probs=[0.2, 0.2], is_put=True, is_american=False)
        eu_put_price = eu_put_option.price()
        self.assertAlmostEqual(eu_put_price, 4.1926542806038585, 10)

    def test_european_call(self):
        """
        Test for European call option, and call-put parity
        """
        eu_call_option = BinomialTreeOption(initial_price=50, strike=52, int_rate=0.05, maturity=2,
                                            steps=2, probs=[0.2, 0.2], is_put=False, is_american=False)
        eu_call_price = eu_call_option.price()

        eu_put_option = BinomialTreeOption(initial_price=50, strike=52, int_rate=0.05, maturity=2,
                                           steps=2, probs=[0.2, 0.2], is_put=True, is_american=False)
        eu_put_price = eu_put_option.price()

        self.assertAlmostEqual(eu_call_price - eu_put_price - (50 - 52/np.exp(0.05 * 2)), 0, 10)

    def test_american_put(self):
        """
        Test for American put option
        """
        am_put_option = BinomialTreeOption(initial_price=50, strike=52, int_rate=0.05, maturity=2,
                                           steps=2, probs=[0.2, 0.2], is_put=True, is_american=True)
        am_put_price = am_put_option.price()

        self.assertAlmostEqual(am_put_price, 5.089632474198373, 10)

    def test_eu_CRR_put(self):
        """
        Test for European put option with the CRR model
        """
        eu_crr_put_option = BinomialCRROption(initial_price=50, strike=52, int_rate=0.05, maturity=2,
                                              steps=2, volatility=0.3, is_put=True, is_american=False)
        eu_crr_put_price = eu_crr_put_option.price()
        self.assertAlmostEqual(eu_crr_put_price, 6.245708445206436, 10)

    def test_am_CRR_put(self):
        """
        Test for American put option with the CRR model
        """
        am_crr_put_option = BinomialCRROption(initial_price=50, strike=52, int_rate=0.05, maturity=2,
                                              steps=2, volatility=0.3, is_put=True, is_american=True)
        am_crr_put_price = am_crr_put_option.price()
        self.assertAlmostEqual(am_crr_put_price, 7.428401902704834, 10)

    def test_eu_LR_put(self):
        """
        Test for European put option with the LR model
        """
        eu_lr_put_option = BinomialLROption(initial_price=50, strike=52, int_rate=0.05, maturity=2,
                                            steps=4, volatility=0.3, is_put=True, is_american=False)
        eu_lr_put_price = eu_lr_put_option.price()
        self.assertAlmostEqual(eu_lr_put_price, 5.878650106601964, 10)

    def test_am_LR_put(self):
        """
        Test for American put option with the LR model
        """
        am_lr_put_option = BinomialLROption(initial_price=50, strike=52, int_rate=0.05, maturity=2,
                                            steps=4, volatility=0.3, is_put=True, is_american=True)
        am_lr_put_price = am_lr_put_option.price()
        self.assertAlmostEqual(am_lr_put_price, 6.763641952939979, 10)

    def test_eu_call_price_tree(self):
        """
        Tests the pricing tree for a European call option
        """
        results = [[34.0796], [60.4959, 2.9752], [107.2727, 5.4545, 0], [190, 10, 0, 0]]
        eu_call_option = BinomialTreeOption(initial_price=80, strike=80, int_rate=np.log(1.1),
                                            maturity=3, steps=3, probs=[0.5, 0.5])
        _ = eu_call_option.price()
        self.assertTrue(utils.lists_are_almost_equal(results, eu_call_option.payoff_tree, 4))

    def test_futures(self):
        """
        Tests the pricing for a futures contract
        """
        price_tree = [[100], [115, 87], [133, 100, 75], [152, 115, 87, 65]]
        int_rates_tree = [[0.02469261], [0.01980263, 0.0295588], [0.00995033, 0.02469261, 0.03440143]]
        futures_contract = BinomialTreeFutures(price_tree=price_tree, int_rates_tree=int_rates_tree, maturity=3)
        _ = futures_contract.price()
        self.assertAlmostEqual(futures_contract.premium, 107.12, 2)


if __name__ == '__main__':
    unittest.main()
