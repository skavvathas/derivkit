import numpy as np
from .utils import N, n
from .black_scholes import d1, d2


# Delta of an option
# @param S: current spot price
# @param K: strike price
# @param T: time to expiration
# @param r: risk-free interest rate
# @param sigma: volatility
# @param option_type: 'call' or 'put'
# @return: delta
def delta(S, K, T, r, sigma, option_type='call'):
    if option_type == 'call':
        return N(d1(S, K, T, r, sigma))
    elif option_type == 'put':
        return N(d1(S, K, T, r, sigma)) - 1
    else:
        raise ValueError("option_type must be 'call' or 'put'")


# Gamma of an option
# @param S: current spot price
# @param K: strike price
# @param T: time to expiration
# @param r: risk-free interest rate
# @param sigma: volatility
# @return: gamma
def gamma(S, K, T, r, sigma):
    return n(d1(S, K, T, r, sigma)) / (S * sigma * np.sqrt(T))


# Vega of an option
# @param S: current spot price
# @param K: strike price
# @param T: time to expiration
# @param r: risk-free interest rate
# @param sigma: volatility
# @return: vega
def vega(S, K, T, r, sigma):
    return S * n(d1(S, K, T, r, sigma)) * np.sqrt(T)


# Theta of an option
# @param S: current spot price
# @param K: strike price
# @param T: time to expiration
# @param r: risk-free interest rate
# @param sigma: volatility
# @param option_type: 'call' or 'put'
# @return: theta
def theta(S, K, T, r, sigma, option_type='call'):
    if option_type == 'call':
        return (-S * n(d1(S, K, T, r, sigma)) * sigma / (2 * np.sqrt(T))
                + r * K * np.exp(-r * T) * N(d2(S, K, T, r, sigma)))
    elif option_type == 'put':
        return (-S * n(d1(S, K, T, r, sigma)) * sigma / (2 * np.sqrt(T))
                - r * K * np.exp(-r * T) * N(-d2(S, K, T, r, sigma)))
    else:
        raise ValueError("option_type must be 'call' or 'put'")


# Rho of an option
# @param S: current spot price
# @param K: strike price
# @param T: time to expiration
# @param r: risk-free interest rate
# @param sigma: volatility
# @param option_type: 'call' or 'put'
# @return: rho
def rho(S, K, T, r, sigma, option_type='call'):
    if option_type == 'call':
        return K * T * np.exp(-r * T) * N(d2(S, K, T, r, sigma))
    elif option_type == 'put':
        return -K * T * np.exp(-r * T) * N(-d2(S, K, T, r, sigma))
    else:
        raise ValueError("option_type must be 'call' or 'put'")
