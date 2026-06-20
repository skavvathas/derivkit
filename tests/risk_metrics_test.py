import numpy as np
from derivkit import (
    max_drawdown,
    sharpe_ratio,
    sortino_ratio,
    parametric_var,
    implied_volatility_raphson_newton_method,
    implied_volatility_bisection,
    implied_volatility_brent,
)

# Price series and the corresponding simple returns
prices = np.array([100, 120, 90, 110, 80, 130], dtype=float)
returns = np.diff(prices) / prices[:-1]

print('Max Drawdown:', max_drawdown(prices))
print('Sharpe Ratio:', sharpe_ratio(returns))
print('Sortino Ratio:', sortino_ratio(returns))
print('Parametric VAR:', parametric_var(returns))

# Implied volatility from an observed option price (S, K, T, r as in the other tests)
S, K, T, r = 100, 100, 1, 0.05
market_price = 10.45
print('Implied Volatility Newton-Raphson:',
      implied_volatility_raphson_newton_method(market_price, S, K, T, r, option_type='call'))
print('Implied Volatility Bisection:',
      implied_volatility_bisection(S, K, r, T, market_price, option_type='call'))
print('Implied Volatility Brent:',
      implied_volatility_brent(S, K, r, T, market_price, option_type='call'))
