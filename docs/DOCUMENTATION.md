# derivkit — Documentation

A lightweight Python library for quantitative finance: options pricing, Greeks,
implied & realized volatility, and portfolio risk metrics.

This document describes every public function together with the mathematical
formula it implements, its parameters, and a short usage example.

> **Note on math:** formulas are written in plain-text/Unicode inside code
> blocks so they render in any markdown viewer (including the VS Code preview).

> **Conventions used throughout**
>
> | Symbol | Meaning |
> |---|---|
> | `S` | Current spot price of the underlying |
> | `K` | Strike price |
> | `T` | Time to expiration, in years |
> | `r` | Continuously-compounded risk-free rate (annualized) |
> | `σ` | Volatility (annualized) |
> | `N(·)` | Standard normal cumulative distribution function (CDF) |
> | `n(·)` | Standard normal probability density function (PDF) |
>
> All rates and volatilities are expressed as decimals (e.g. `0.05` = 5%).

---

## Table of contents

1. [Installation](#installation)
2. [Helper functions (`utils`)](#helper-functions-utils)
3. [Black–Scholes pricing](#blackscholes-pricing)
4. [The Greeks](#the-greeks)
5. [Second-order Greeks](#second-order-greeks)
6. [Binomial tree pricing](#binomial-tree-pricing)
7. [Implied volatility](#implied-volatility)
8. [Realized volatility](#realized-volatility)
9. [Risk metrics](#risk-metrics)

---

## Installation

```bash
pip install derivkit
```

Or from source (editable):

```bash
git clone https://github.com/spiroskavvathas/derivkit.git
cd derivkit
pip install -e .
```

Requires Python 3.9+, NumPy, and SciPy.

---

## Helper functions (`utils`)

These underpin the rest of the library.

| Function | Returns |
|---|---|
| `N(x)` | Standard normal CDF |
| `n(x)` | Standard normal PDF |
| `ppf(x)` | Inverse normal CDF (quantile function), `N⁻¹(x)` |

```
N(x) = ∫_{-∞}^{x} (1/√(2π)) · e^(−t²/2) dt
n(x) = (1/√(2π)) · e^(−x²/2)
```

Validation helpers raise `ValueError` on invalid input:

- `validate_input_parameters(S, K, T, r, sigma, option_type)` — enforces
  `S>0`, `K>0`, `T>0`, `r≥0`, `σ>0`, and `option_type ∈ {'call','put'}`.
- `validate_input_parameters_risk_metrics(prices)` — enforces a non-empty 1-D
  NumPy array of positive, finite values.

---

## Black–Scholes pricing

`black_scholes(S, K, T, r, sigma, option_type='call')`

Closed-form price of a European option under the Black–Scholes model.

First define the standardized moneyness terms:

```
d1 = [ ln(S/K) + (r + σ²/2)·T ] / (σ·√T)
d2 = d1 − σ·√T
```

Then the prices are:

```
Call:  C = S·N(d1) − K·e^(−rT)·N(d2)
Put:   P = K·e^(−rT)·N(−d2) − S·N(−d1)
```

The standalone `d1` and `d2` terms are also available as `d1(...)` and
`d2(...)` in `derivkit.black_scholes`.

```python
from derivkit import black_scholes

black_scholes(S=100, K=100, T=1.0, r=0.05, sigma=0.2, option_type='call')
# 10.4506
```

---

## The Greeks

Sensitivities of the Black–Scholes price to its inputs. All take the same core
signature `(S, K, T, r, sigma[, option_type])`.

### Delta — ∂V/∂S

`delta(S, K, T, r, sigma, option_type='call')`

```
Delta (call) = N(d1)
Delta (put)  = N(d1) − 1
```

### Gamma — ∂²V/∂S²

`gamma(S, K, T, r, sigma)` (same for calls and puts)

```
Gamma = n(d1) / (S·σ·√T)
```

### Vega — ∂V/∂σ

`vega(S, K, T, r, sigma)` (same for calls and puts)

```
Vega = S·n(d1)·√T
```

### Theta — ∂V/∂T (time decay)

`theta(S, K, T, r, sigma, option_type='call')`

```
Theta (call) = −[ S·n(d1)·σ ] / (2·√T) + r·K·e^(−rT)·N(d2)
Theta (put)  = −[ S·n(d1)·σ ] / (2·√T) − r·K·e^(−rT)·N(−d2)
```

### Rho — ∂V/∂r

`rho(S, K, T, r, sigma, option_type='call')`

```
Rho (call) =  K·T·e^(−rT)·N(d2)
Rho (put)  = −K·T·e^(−rT)·N(−d2)
```

```python
from derivkit import delta, gamma, vega, theta, rho

S, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.2
delta(S, K, T, r, sigma, 'call')   # 0.6368
gamma(S, K, T, r, sigma)           # 0.0188
vega(S, K, T, r, sigma)            # 37.52
```

---

## Second-order Greeks

Sensitivities of the *first-order* Greeks — i.e. second derivatives of the
option price. They describe how Delta and Vega themselves move as the spot,
volatility, rate, or time change, which matters for hedging a book over time.

All of these assume the standard Black–Scholes model with **no dividends**.
Under that assumption each value below is identical for calls and puts, so the
functions take only `(S, K, T, r, sigma)` (no `option_type`). They live in
`derivkit.second_greeks`.

### Vanna — ∂Vega/∂S = ∂Delta/∂σ

`vanna(S, K, T, r, sigma)`

```
Vanna = −n(d1)·d2 / σ
```

How Delta responds to a change in volatility (equivalently, how Vega responds
to a change in spot).

### Vomma (Volga) — ∂Vega/∂σ

`vomma(S, K, T, r, sigma)`

```
Vomma = Vega·d1·d2 / σ = S·n(d1)·√T·d1·d2 / σ
```

The convexity of the option value in volatility — how Vega changes as
volatility moves.

### Charm — ∂Delta/∂t (delta decay)

`charm(S, K, T, r, sigma)`

```
Charm = −n(d1)·(2rT − d2·σ·√T) / (2·T·σ·√T)
```

The rate at which Delta drifts as time passes (the `t` here is calendar time,
so this is `−∂Delta/∂T`). Useful for managing the delta of a hedge overnight or
over a weekend.

### Veta — ∂Vega/∂t (vega decay)

`veta(S, K, T, r, sigma)`

```
Veta = −S·n(d1)·√T·[ (1 + d1·d2)/(2T) − r·d1/(σ·√T) ]
```

How Vega decays as time passes (`−∂Vega/∂T`).

### Vera (Rhova) — ∂Vega/∂r = ∂Rho/∂σ

`vera(S, K, T, r, sigma)`

```
Vera = −K·T·e^(−rT)·n(d2)·d1 / σ
```

The cross-sensitivity between volatility and the interest rate.

```python
from derivkit import vanna, vomma, charm, veta, vera

S, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.2
vanna(S, K, T, r, sigma)   # −0.2814
vomma(S, K, T, r, sigma)   #  9.8501
charm(S, K, T, r, sigma)   # −0.0657
veta(S, K, T, r, sigma)    # −16.4637
vera(S, K, T, r, sigma)    # −65.6671
```

---

## Binomial tree pricing

`binomial_tree(S, K, T, r, sigma, n, option_type='call', style='european')`

Cox–Ross–Rubinstein (CRR) lattice. Supports **European** and **American**
exercise. With `n` time steps and step size `Δt = T/n`:

```
Δt = T / n
u  = e^(σ·√Δt)            (up factor)
d  = 1 / u                (down factor)
p  = (e^(r·Δt) − d) / (u − d)   (risk-neutral prob. of an up-move)
```

Terminal payoffs at the leaves `S_T = S · u^(n−j) · d^j`:

```
Call: max(S_T − K, 0)
Put : max(K − S_T, 0)
```

Values are rolled back through the tree by discounted risk-neutral expectation:

```
V_i = e^(−r·Δt) · [ p·V_up + (1−p)·V_down ]
```

For **American** style, at each node the rolled-back value is compared against
the intrinsic value and the larger is kept (early exercise):

```
V_i = max( V_i, intrinsic_i )
```

As `n → ∞` the European price converges to the Black–Scholes value.

```python
from derivkit import binomial_tree

binomial_tree(S=100, K=100, T=1.0, r=0.05, sigma=0.2,
              n=500, option_type='put', style='american')
```

---

## Implied volatility

Given an observed market price, solve for the `σ` that makes the Black–Scholes
price match. Formally, find the root of:

```
f(σ) = BS(S, K, T, r, σ) − market_price = 0
```

Because the Black–Scholes price is strictly increasing in `σ`, the root is
unique. Three solvers are provided (in `derivkit.risk_metrics`):

### Newton–Raphson

`implied_volatility_raphson_newton_method(price, S, K, T, r, option_type='call', max_iterations=100, tolerance=1e-6)`

Iterates using the derivative (vega):

```
σ_{k+1} = σ_k − f(σ_k) / Vega(σ_k)
```

Fast (quadratic convergence) but relies on a good starting guess and a non-zero
vega.

### Bisection

`implied_volatility_bisection(S, K, r, T, market_price, option_type='call', tol=1e-7, max_iterations=100)`

Brackets the root in `σ ∈ [1e−6, 10]` and repeatedly halves the interval,
keeping the half that still contains the root. Slower but guaranteed to
converge.

### Brent's method

`implied_volatility_brent(S, K, r, T, market_price, option_type='call', tol=1e-7)`

Combines bisection with inverse quadratic interpolation (via
`scipy.optimize.brentq`) over the same bracket — robust *and* fast.

```python
from derivkit.black_scholes import black_scholes
from derivkit.risk_metrics import (
    implied_volatility_bisection,
    implied_volatility_brent,
)

price = black_scholes(S=100, K=100, T=1.0, r=0.05, sigma=0.2, option_type='call')
implied_volatility_bisection(S=100, K=100, r=0.05, T=1.0, market_price=price)  # ≈ 0.20
implied_volatility_brent(S=100, K=100, r=0.05, T=1.0, market_price=price)      # ≈ 0.20
```

> **Note on argument order:** the bisection and Brent solvers take
> `(S, K, r, T, market_price, ...)`, whereas the Newton–Raphson solver takes
> `(price, S, K, T, r, ...)`.

---

## Realized volatility

`realized_volatility(prices, window=20)`

Annualized rolling standard deviation of log returns. From a price series
`P_0, P_1, …`:

```
log return:    r_t = ln( P_t / P_{t−1} )
realized vol:  σ = √252 · std( r_{t−w+1}, …, r_t )      (window length w)
```

Returns a NumPy array of rolling values (or `nan` if there are fewer returns
than the window).

```python
import numpy as np
from derivkit import realized_volatility

prices = np.array([100, 102, 101, 105, 103, 108, 107, 110])
realized_volatility(prices, window=3)
```

---

## Risk metrics

Portfolio/return-series statistics. `returns` and `prices` are 1-D NumPy arrays.

### Parametric Value at Risk

`parametric_var(returns, confidence=0.95)`

Variance–covariance (Gaussian) VaR. With sample mean `μ`, standard deviation
`σ`, and the normal quantile `z = N⁻¹(confidence)`:

```
VaR = −( μ − z·σ )
```

Reported as a positive number representing the loss at the given confidence
level.

### Sharpe ratio

`sharpe_ratio(returns, rf=0.0, periods=252)`

Annualized excess return per unit of total risk:

```
Sharpe = ( mean(r)·periods − rf ) / ( std(r)·√periods )
```

### Sortino ratio

`sortino_ratio(returns, rf=0.0, periods=252)`

Like Sharpe, but penalizes only downside volatility (the standard deviation of
negative returns, `std_downside`):

```
Sortino = ( mean(r)·periods − rf ) / ( std_downside·√periods )
```

### Maximum drawdown

`max_drawdown(prices)`

Largest peak-to-trough decline as a fraction. With the running peak
`Peak_t = max over s≤t of P_s`:

```
MaxDD = min over t of [ (P_t − Peak_t) / Peak_t ]
```

Returns a non-positive number (e.g. `-0.25` = a 25% drawdown).

```python
import numpy as np
from derivkit import parametric_var, sharpe_ratio, sortino_ratio, max_drawdown

prices = np.array([100, 102, 99, 104, 101, 107, 103])
returns = np.diff(np.log(prices))

parametric_var(returns, confidence=0.95)
sharpe_ratio(returns, rf=0.0)
sortino_ratio(returns, rf=0.0)
max_drawdown(prices)
```

---

## See also

- `README.md` — quick start and feature overview.
- `tests/` — worked examples of every function.
