import numpy as np
from .utils import N

# Black-Scholes d1 formula
# @param S: current spot price
# @param K: strike price
# @param T: time to expiration
# @param r: risk-free interest rate
# @param sigma: volatility
# @return: d1
def d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))


# Black-Scholes d2 formula
# @param S: current spot price
# @param K: strike price
# @param T: time to expiration
# @param r: risk-free interest rate
# @param sigma: volatility
# @return: d2
def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)


# Black-Scholes price for European call/put
# @param S: current spot price
# @param K: strike price
# @param T: time to expiration
# @param r: risk-free interest rate
# @param sigma: volatility
# @param option_type: 'call' or 'put'
# @return: price
def black_scholes(S, K, T, r, sigma, option_type='call'):
    if option_type == 'call':
        return S * N(d1(S, K, T, r, sigma)) - K * np.exp(-r * T) * N(d2(S, K, T, r, sigma))
    elif option_type == 'put':
        return K * np.exp(-r * T) * N(-d2(S, K, T, r, sigma)) - S * N(-d1(S, K, T, r, sigma))
    else:
        raise ValueError("option_type must be 'call' or 'put'")
