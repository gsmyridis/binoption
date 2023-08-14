import binompricer as bp

"""
Examples of how to use the package. You can also chech out the tests folder.
"""

if __name__ == '__main__':
    eu_put_100 = bp.BinomialTreeOption(strike=105,
                                       maturity=3,
                                       initial_price=90,
                                       steps=3,
                                       price_changes=[1.1, 0.9],
                                       tree_method='multiply',
                                       int_rate=0.0554,
                                       is_put=False,
                                       is_american=False)
    eu_put_100.price()
    print(eu_put_100.risk_free_probs_up)
    print("Premium:", eu_put_100.premium)

