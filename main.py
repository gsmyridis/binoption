import binompricer as bp

"""
Examples of how to use the package. You can also chech out the tests folder.
"""

if __name__ == '__main__':

    eu_put_option = bp.BinomialTreeOption(initial_price=100,
                                          strike=105,
                                          int_rate=0.05,
                                          maturity=4,
                                          steps=4,
                                          price_changes=[1.2, 0.8],
                                          tree_method='multiply',
                                          is_put=True,
                                          is_american=False)
    eu_put_price = eu_put_option.price()
    print("European 105-Put:", eu_put_price)

    am_put_option = bp.BinomialTreeOption(initial_price=100,
                                          strike=105,
                                          int_rate=0.05,
                                          maturity=4,
                                          steps=4,
                                          price_changes=[1.2, 0.8],
                                          tree_method='multiply',
                                          is_put=True,
                                          is_american=True)
    am_put_price = am_put_option.price()
    print("American 105-put:", am_put_price)
