# derivkit

A lightweight Python library for quantitative finance — options pricing, Greeks, volatility, and risk metrics.

```python
from derivkit import black_scholes, delta

price = black_scholes(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type='call')  # 10.45
d = delta(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type='call')              # 0.637
```

---

## Installation

Install from PyPI:

```bash
pip install derivkit
```

Or install locally from source (editable mode):

```bash
git clone https://github.com/spiroskavvathas/derivkit.git
cd derivkit
pip install -e .
```

Requires Python 3.9+, NumPy, and SciPy.

---

## What's inside

### Options Pricing

| Function | Description |
|---|---|
| `black_scholes(S, K, T, r, sigma, option_type)` | Black-Scholes price for European call/put |
| `binomial_tree(S, K, T, r, sigma, n, option_type, style)` | Binomial tree model (CRR), European or American |

### Greeks

| Function | Description |
|---|---|
| `delta(S, K, T, r, sigma, option_type)` | First-order sensitivity to spot price |
| `gamma(S, K, T, r, sigma)` | Second-order sensitivity to spot price |
| `vega(S, K, T, r, sigma)` | Sensitivity to volatility |
| `theta(S, K, T, r, sigma, option_type)` | Sensitivity to time decay |
| `rho(S, K, T, r, sigma, option_type)` | Sensitivity to interest rate |

### Volatility

| Function | Description |
|---|---|
| `realized_volatility(prices, window)` | Realized (historical) vol from a price series |

### Risk Metrics

| Function | Description |
|---|---|
| `parametric_var(returns, confidence)` | Value at Risk (parametric / variance-covariance) |
| `sharpe_ratio(returns, rf, periods)` | Annualized Sharpe ratio |
| `sortino_ratio(returns, rf, periods)` | Annualized Sortino ratio |
| `max_drawdown(prices)` | Maximum peak-to-trough drawdown |

---

## Quick start

### Price an option and compute all Greeks

```python
from derivkit import black_scholes, delta, gamma, vega, theta, rho

S, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.2

print("Price :", black_scholes(S, K, T, r, sigma, option_type='call'))
print("Delta :", delta(S, K, T, r, sigma, option_type='call'))
print("Gamma :", gamma(S, K, T, r, sigma))
print("Vega  :", vega(S, K, T, r, sigma))
print("Theta :", theta(S, K, T, r, sigma, option_type='call'))
print("Rho   :", rho(S, K, T, r, sigma, option_type='call'))
```

### Price an American option with a binomial tree

```python
from derivkit import binomial_tree

price = binomial_tree(S=100, K=100, T=1.0, r=0.05, sigma=0.2,
                      n=500, option_type='put', style='american')
print("American put:", price)
```

### Risk metrics on a returns series

```python
import numpy as np
from derivkit import parametric_var, sharpe_ratio, max_drawdown

prices = np.array([100, 102, 99, 104, 101, 107, 103])
returns = np.diff(np.log(prices))

print("VaR 95% :", parametric_var(returns, confidence=0.95))
print("Sharpe  :", sharpe_ratio(returns, rf=0.0))
print("Max DD  :", max_drawdown(prices))
```

---

## Parameters

The pricing and Greek functions share the same core signature:

| Parameter | Description |
|---|---|
| `S` | Current spot price of the underlying |
| `K` | Strike price |
| `T` | Time to expiration in years (e.g. `0.25` = 3 months) |
| `r` | Risk-free interest rate (annualized, e.g. `0.05` = 5%) |
| `sigma` | Volatility (annualized, e.g. `0.2` = 20%) |
| `option_type` | `'call'` or `'put'` |

`binomial_tree` additionally takes `n` (number of steps) and `style` (`'european'` or `'american'`).

---

## Roadmap

- [x] Black-Scholes pricing
- [x] First-order Greeks (delta, gamma, vega, theta, rho)
- [x] Binomial tree pricing (CRR), European & American
- [x] Realized volatility
- [x] VaR / Sharpe / Sortino / max drawdown
- [ ] Monte Carlo simulation
- [ ] Implied volatility solver
- [ ] Parkinson volatility
- [ ] CVaR (expected shortfall)
- [ ] Second-order Greeks (vanna, volga, charm)
- [ ] Fixed income: bond price, duration, convexity, YTM
- [ ] NumPy vectorized inputs (batch computation)
- [ ] Heston stochastic volatility model

---

## Contributing

Pull requests are welcome. To add a new function:

1. Add the implementation under `derivkit/`
2. Export it from `derivkit/__init__.py`
3. Add a usage example to `examples/`

---

## License

MIT
