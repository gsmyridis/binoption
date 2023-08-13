import unittest
import sys
import os
# Get the path to the parent directory (project directory)
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the project directory to the Python path
sys.path.insert(0, project_dir)

from binompricer import Stock

err_no_tree = ("If no stock 'price_tree' is provided, then 'initial_price' and 'steps' "
               "must be specified, along with 'probs' or 'price_changes'.")
price_tree = [[1], [1, 2], [1, 2, 3]]


class StockTest(unittest.TestCase):
    def test_no_initial_price(self):
        """
        Test for ValueError when no initial price
        and no price tree is provided at initialisation
        of a stock instance
        """
        with self.assertRaisesRegex(ValueError, err_no_tree):
            _ = Stock(initial_price=None, price_tree=None, probs=[0.5, 0.5])

    def test_no_steps(self):
        """
        Test for ValueError when no initial price tree
        and no number of steps is provided at initialisation
        """
        with self.assertRaisesRegex(ValueError, err_no_tree):
            _ = Stock(initial_price=100, steps=None, probs=[0.5, 0.5])

    def test_probs_price_changes(self):
        """
        Test for ValueError when neither of both of
        price_changes and probs are secified, at initialisation
        """
        with self.assertRaisesRegex(ValueError, err_no_tree):
            _ = Stock(initial_price=100)
        with self.assertRaisesRegex(ValueError, "You can specify either 'probs' or 'price_changes', not both."):
            _ = Stock(initial_price=100, probs=[0.5, 0.5], price_changes=[1, 1])

    def test_probs_values(self):
        """
        Test for ValueError when probs are specified
        but either entry in None, or when both are zero
        """
        with self.assertRaisesRegex(ValueError, err_no_tree):
            _ = Stock(initial_price=100, probs=[None, 0.5])
        with self.assertRaisesRegex(ValueError, err_no_tree):
            _ = Stock(initial_price=100, probs=[0.5, None])
        with self.assertRaisesRegex(ValueError, "When you specify probs, they cannot both be zero."):
            _ = Stock(initial_price=100, probs=[0, 0])

    def test_price_changes_values(self):
        """
        Test for ValueError when price_changes are specified
        but either entry is None, or both are zero
        """
        with self.assertRaisesRegex(ValueError, err_no_tree):
            _ = Stock(initial_price=100, price_changes=[None, 1])
        with self.assertRaisesRegex(ValueError, err_no_tree):
            _ = Stock(initial_price=100, price_changes=[1, None])
        with self.assertRaisesRegex(ValueError, "When you specify price_changes, they cannot be both zero."):
            _ = Stock(initial_price=100, price_changes=[0, 0])

    def test_non_positive_maturity(self):
        """
        Test for ValueError when maturity time is non-positive
        """
        with self.assertRaisesRegex(ValueError, "Maturity time has to be larger than zero."):
            _ = Stock(initial_price=100, maturity=0, probs=[0.5, 0.5])
        with self.assertRaisesRegex(ValueError, "Maturity time has to be larger than zero."):
            _ = Stock(initial_price=100, maturity=-1, probs=[0.5, 0.5])

    def test_tree_method_value(self):
        """
        Test for ValueError when tree method is not in ['direct', 'multiply', 'add']
        or when it is 'direct' but no price tree is provided
        """
        with self.assertRaisesRegex(ValueError, "Tree_method can only be 'multiply', 'add' or 'direct'."):
            _ = Stock(initial_price=100, probs=[0.5, 0.5], tree_method='method')
        with self.assertRaisesRegex(ValueError, "Your tree_method is 'direct',"
                                                " but you have not provided a price_tree."):
            _ = Stock(initial_price=100, probs=[0.5, 0.5], tree_method='direct')

    def test_recombining_price_tree(self):
        """
        Test for ValueError when the tree format is not correct for recombining trees
        That is, when the length of the prices does not start with a single price
        and increase by one each time
        """
        err_recomb_tree_nodes = ("Assuming the tree is recombining, the number of nodes"
                                 " should start from one and increase by one.")
        with self.assertRaisesRegex(ValueError, err_recomb_tree_nodes):
            _ = Stock(price_tree=[[1], [2, 3, 4]])
        with self.assertRaisesRegex(ValueError, "The price tree cannot be of zero length."):
            _ = Stock(price_tree=[])

    def test_pu_pd_values(self):
        """
        Test for ValueError when the values of the probabilities to the
        up-state or down-state do not lie in [0,1]
        """

        with self.assertRaisesRegex(ValueError, "Probabilities have to lie in the range from 0 to 1."):
            _ = Stock(initial_price=100, steps=3, probs=[-0.5, 0.5])
        with self.assertRaisesRegex(ValueError, "Probabilities have to lie in the range from 0 to 1."):
            _ = Stock(initial_price=100, steps=3, probs=[0.5, -0.5])
        with self.assertRaisesRegex(ValueError, "Probabilities have to lie in the range from 0 to 1."):
            _ = Stock(initial_price=100, steps=3, probs=[-0.5, -0.5])

    def test_u_d_values(self):
        """
        Test for ValueError when the values of the price changes u, or d to the
        up-state or down-state respectively are negative
        """
        with self.assertRaisesRegex(ValueError, "Factors and summands have to be non-negative."):
            _ = Stock(initial_price=100, price_changes=[1, -1])
        with self.assertRaisesRegex(ValueError, "Factors and summands have to be non-negative."):
            _ = Stock(initial_price=100, price_changes=[-1, 1])

    def test_set_price_tree(self):
        """
        Test for change of attributes when providing a price_tree
        """
        call = Stock(initial_price=100, price_tree=price_tree, steps=1, tree_method='add')
        # Test change of steps
        self.assertEqual(call.steps, len(price_tree) - 1)
        # Test change of tree method
        self.assertEqual(call.tree_method, 'direct')
        # Test change of initial price
        self.assertEqual(call.initial_price, price_tree[0][0])
        # Test change of price tree

    def test_no_interest_rate(self):
        """ Test for ValueError when no int_rate and no int_rates_tree is provided """
        with self.assertRaisesRegex(ValueError, "If no 'int_rates_tree' is provided, 'int_rate' has to be specified."):
            _ = Stock(price_tree=price_tree, int_rate=None)

    def test_interest_rates_tree(self):
        """ Test for ValueError when the structure of interest rates tree is not correct """
        int_rates_tree1 = [[0.1], [0.1, 0.2, 0.3], [0.1, 0.2, 0.3]]
        int_rates_tree2 = [[0.1]]
        with self.assertRaisesRegex(ValueError, "Assuming the tree is recombining, the number of nodes"
                                    " should start from one and increase by one."):
            _ = Stock(price_tree=price_tree, int_rates_tree=int_rates_tree1)

        with self.assertRaisesRegex(ValueError, "The 'int_rates_tree' must have length at least equal to 'steps' - 1."):
            _ = Stock(price_tree=price_tree, int_rates_tree=int_rates_tree2)


if __name__ == '__main__':
    unittest.main()
