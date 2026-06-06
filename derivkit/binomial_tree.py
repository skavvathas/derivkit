import numpy as np
from .utils import validate_input_parameters

# Binomial tree model for pricing options
# @param S: current spot price
# @param K: strike price
# @param T: time to expiration
# @param r: risk-free interest rate
# @param sigma: volatility
# @param n: number of steps
# @param option_type: 'call' or 'put'
# @param style: 'european' or 'american'
# @return: price
def binomial_tree(S, K, T, r, sigma, n, option_type='call', style='european'):
    # Validate input parameters
    validate_input_parameters(S, K, T, r, sigma, option_type)

    dt = T / n
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)

    j = np.arange(n + 1)
    ST = S * (u ** (n - j)) * (d ** j)

    if option_type == 'call':
        values = np.maximum(ST - K, 0)
    elif option_type == 'put':
        values = np.maximum(K - ST, 0)

    for i in range(n - 1, -1, -1):
        values = discount * (p * values[:-1] + (1 - p) * values[1:])

        if style == 'american':
            Si = S * (u ** np.arange(i + 1)) * (d ** np.arange(i, -1, -1))
            if option_type == 'call':
                intrinsic = np.maximum(Si - K, 0)
            else:
                intrinsic = np.maximum(K - Si, 0)
            values = np.maximum(values, intrinsic)
        elif style != 'european':
            raise ValueError("style must be 'european' or 'american'")

    return values[0]
