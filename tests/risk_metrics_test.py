from derivkit import max_drawdown, sharpe_ratio, sortino_ratio, parametric_var, implied_volatility_raphson_newton_method

prices = [100, 120, 90, 110, 80, 130]

print('Max Drawdown:', max_drawdown(prices))
print('Sharpe Ratio:', sharpe_ratio(prices))
print('Sortino Ratio:', sortino_ratio(prices))
print('Parametric VAR:', parametric_var(prices))
print('Implied Volatility Newton-Raphson:', implied_volatility_raphson_newton_method(prices))