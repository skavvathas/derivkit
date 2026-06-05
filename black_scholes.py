import numpy as np
from utils import N

def d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

def black_scholes(S, K, T, r, sigma, type):
    if type == 'call':
        return S * N(d1(S, K, T, r, sigma)) - K * np.exp(-r * T) * N(d2(S, K, T, r, sigma))
    elif type == 'put':
        return K * np.exp(-r * T) * N(-d2(S, K, T, r, sigma)) - S * N(-d1(S, K, T, r, sigma))
    else:
        raise ValueError("Invalid option type")