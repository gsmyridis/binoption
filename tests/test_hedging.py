import unittest
import os
import sys

import numpy as np

import utils

# Get the path to the parent directory (project directory)
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the project directory to the Python path
sys.path.insert(0, project_dir)

from binompricer import BinomialTreeOption


class MyTestCase(unittest.TestCase):

    def test_hedge_ratio(self):
        """
        Tests the hedging ratio tree for a European call option
        """
        results = [[0.7190], [0.8485, 0.1364], [1., 0.1667, 0.]]
        eu_call_option = BinomialTreeOption(initial_price=80, strike=80, int_rate=np.log(1.1),
                                            maturity=3, steps=3, probs=[0.5, 0.5])
        _ = eu_call_option.price()
        eu_call_hedge_ratios = eu_call_option.calc_hedge_ratios()
        self.assertTrue(utils.lists_are_almost_equal(results, eu_call_hedge_ratios, 4))


if __name__ == '__main__':
    unittest.main()
