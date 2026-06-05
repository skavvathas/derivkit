import numpy as np
from utils import N, n
from black_scholes import d1, d2

# Delta is the first derivative of the option price with respect to the underlying asset price
def delta(S, K, T, r, sigma, type):
    if type == 'call':
        return N(d1(S, K, T, r, sigma))
    elif type == 'put':
        return N(d1(S, K, T, r, sigma)) - 1
    else:
        raise ValueError("Invalid option type")

# Gamma is the second derivative of the option price with respect to the underlying asset price
def gamma(S, K, T, r, sigma, type):
    return n(d1(S, K, T, r, sigma)) / (S * sigma * np.sqrt(T))

# Vega is the first derivative of the option price with respect to the underlying asset's volatility
def vega(S, K, T, r, sigma, type):
    return S * n(d1(S, K, T, r, sigma)) * np.sqrt(T)

# Theta is the first derivative of the option price with respect to the time to expiration
def theta(S, K, T, r, sigma, type):
    if type == 'call':
        return -S * n(d1(S, K, T, r, sigma)) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * N(d2(S, K, T, r, sigma))
    elif type == 'put':
        return -S * n(d1(S, K, T, r, sigma)) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * N(-d2(S, K, T, r, sigma))
    else:
        raise ValueError("Invalid option type")

# Rho is the first derivative of the option price with respect to the risk-free interest rate
def rho(S, K, T, r, sigma, type):
    if type == 'call':
        return K * T * np.exp(-r * T) * N(d2(S, K, T, r, sigma))
    elif type == 'put':
        return -K * T * np.exp(-r * T) * N(-d2(S, K, T, r, sigma))
    else:
        raise ValueError("Invalid option type")