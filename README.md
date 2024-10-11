# Binomial Pricer
The package offers the ability to price European and American options as well as futures contracts with a binomial tree. In the current version, only recombining trees are supported.

## Option Pricing
Option pricing is carried out with the base class `BinomialTreeOption`
```python 
BinomialTreeOption(strike,
                   maturity,
                   initial_price=None,
                   price_tree=None,
                   steps=2,
                   probs=[None, None],
                   price_changes=[None, None],
                   tree_method='multiply',
                   int_rate=0.05,
                   int_rates_tree=None,
                   volatility=0,
                   dividents=0,
                   is_put=False,
                   is_american=False)           
```

At initialisation, the class has to be provided with:
1. The `strike` price and the `maturity` of the option.
2. **Price tree**: The recombining price tree for the underlying option can be specified in different ways.
One way is to provide the `price_tree` directly. The other ways, are to provide an `initial_price`,
along with the probabilities `probs` to transition to the [up-state, down-state] or to provide the
`price_changes` for these transitions. Another parameter that has to be specified in this case is the
`tree_method`, `='multiply'` if at each time steps we multiply the current price with the `price_changes`
and `='add'` if we add them. 
3.  **Interest**: The interest rate at each node of the tree can be specified again with eitther of the two ways;
by providint a constant `int_rate`, or specifiying the `int_rates_tree` directly.
4. If the option `is_put` and if it `is_american`.

### Examples
More examples can be found in the `tests/` directory.

Assume we have a stock with current price $105, and according to our model,
at each step its value either increases by a factor of 1.2
or falls by a factor of 0.8 (with risk neutral probabilities).
We want to price a European and an American put option with strike price $105 and maturity 2 years with 2 steps.
The interest rate is constant and equal to 0.05.
```python
import binompricer as bp
eu_put_option = bp.BinomialTreeOption(initial_price=100,
                                      strike=105,
                                      int_rate=0.05,
                                      maturity=2,
                                      steps=2,
                                      price_changes=[1.2, 0.8],
                                      tree_method='multiply',
                                      is_put=True,
                                      is_american=False)
eu_put_price = eu_put_option.price()
print("European 105-Put:", eu_put_price)

am_put_option = bp.BinomialTreeOption(initial_price=100,
                                      strike=105,
                                      int_rate=0.05,
                                      maturity=2,
                                      steps=2,
                                      price_changes=[1.2, 0.8],
                                      tree_method='multiply',
                                      is_put=True,
                                      is_american=True)
am_put_price = am_put_option.price()
print("American 105-put:", am_put_price)
```
```
European 105-Put: 8.933090552106973
American 105-put: 10.74429651994205
```

