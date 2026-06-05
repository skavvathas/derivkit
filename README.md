# derivkit

A lightweight Python library for quantitative finance — options pricing, Greeks, volatility tools, and risk metrics.

```python
from derivkit import black_scholes, delta, implied_volatility, var

price = black_scholes(S=100, K=100, T=1, r=0.05, sigma=0.2, type='call')  # 10.45
d = delta(S=100, K=100, T=1, r=0.05, sigma=0.2, type='call')              # 0.637
```

---

## Installation

```bash
pip install derivkit
```

Requires Python 3.8+ and NumPy.

---

## What's inside

### Options Pricing

| Function | Description |
|---|---|
| `black_scholes(S, K, T, r, sigma, type)` | Black-Scholes price for European call/put |
| `binomial_tree(S, K, T, r, sigma, type, n)` | Binomial tree model (CRR) |
| `monte_carlo(S, K, T, r, sigma, type, n_sims)` | Monte Carlo simulation price |

### Greeks

| Function | Description |
|---|---|
| `delta(S, K, T, r, sigma, type)` | First-order sensitivity to spot price |
| `gamma(S, K, T, r, sigma, type)` | Second-order sensitivity to spot price |
| `vega(S, K, T, r, sigma, type)` | Sensitivity to volatility |
| `theta(S, K, T, r, sigma, type)` | Sensitivity to time decay |
| `rho(S, K, T, r, sigma, type)` | Sensitivity to interest rate |
| `vanna(S, K, T, r, sigma, type)` | Cross-derivative: delta w.r.t. vol |
| `volga(S, K, T, r, sigma, type)` | Second-order sensitivity to volatility |

### Volatility

| Function | Description |
|---|---|
| `implied_volatility(price, S, K, T, r, type)` | IV via Newton-Raphson |
| `historical_volatility(prices, window)` | Realized vol from a price series |
| `parkinson_volatility(high, low)` | Range-based volatility estimator |

### Risk Metrics

| Function | Description |
|---|---|
| `var(returns, confidence)` | Value at Risk (parametric & historical) |
| `cvar(returns, confidence)` | Conditional VaR (Expected Shortfall) |
| `sharpe(returns, rf)` | Sharpe ratio |
| `sortino(returns, rf)` | Sortino ratio |
| `max_drawdown(prices)` | Maximum peak-to-trough drawdown |

### Fixed Income *(coming soon)*

| Function | Description |
|---|---|
| `bond_price(face, coupon, T, ytm)` | Present value of a bond |
| `duration(face, coupon, T, ytm)` | Macaulay duration |
| `convexity(face, coupon, T, ytm)` | Convexity of a bond |
| `yield_to_maturity(price, face, coupon, T)` | YTM via numerical solver |

---

## Quick start

### Price an option and compute all Greeks

```python
from derivkit import black_scholes, delta, gamma, vega, theta, rho

S, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.2

print("Price :", black_scholes(S, K, T, r, sigma, type='call'))
print("Delta :", delta(S, K, T, r, sigma, type='call'))
print("Gamma :", gamma(S, K, T, r, sigma, type='call'))
print("Vega  :", vega(S, K, T, r, sigma, type='call'))
print("Theta :", theta(S, K, T, r, sigma, type='call'))
print("Rho   :", rho(S, K, T, r, sigma, type='call'))
```

### Compute implied volatility from a market price

```python
from derivkit import implied_volatility

market_price = 10.45
iv = implied_volatility(price=market_price, S=100, K=100, T=1.0, r=0.05, type='call')
print(f"Implied vol: {iv:.2%}")  # 20.00%
```

### Risk metrics on a returns series

```python
import numpy as np
from derivkit import var, cvar, sharpe, max_drawdown

prices = np.array([100, 102, 99, 104, 101, 107, 103])
returns = np.diff(np.log(prices))

print("VaR 95%  :", var(returns, confidence=0.95))
print("CVaR 95% :", cvar(returns, confidence=0.95))
print("Sharpe   :", sharpe(returns, rf=0.0))
```

---

## Parameters

All pricing and Greek functions share the same signature:

| Parameter | Description |
|---|---|
| `S` | Current spot price of the underlying |
| `K` | Strike price |
| `T` | Time to expiration in years (e.g. `0.25` = 3 months) |
| `r` | Risk-free interest rate (annualized, e.g. `0.05` = 5%) |
| `sigma` | Volatility (annualized, e.g. `0.2` = 20%) |
| `type` | `'call'` or `'put'` |

---

## Roadmap

- [ ] Binomial tree pricing (CRR)
- [ ] Monte Carlo simulation
- [ ] Implied volatility solver
- [ ] Historical & Parkinson volatility
- [ ] VaR / CVaR / Sharpe / Sortino
- [ ] Maximum drawdown
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
