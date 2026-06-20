import numpy as np
from .utils import n, validate_input_parameters
from .black_scholes import d1, d2

# Second-order Greeks (sensitivities of the first-order Greeks).
#
# All formulas below assume the standard Black-Scholes model with no dividends.
# Under this assumption every second-order Greek implemented here is identical
# for calls and puts, so none of them take an `option_type` argument.


# Vanna of an option
# Vanna = d(Vega)/dS = d(Delta)/dsigma = d^2 V / (dS dsigma)
# @param S: current spot price
# @param K: strike price
# @param T: time to expiration
# @param r: risk-free interest rate
# @param sigma: volatility
# @return: vanna
def vanna(S, K, T, r, sigma):
    # Validate input parameters
    validate_input_parameters(S, K, T, r, sigma)

    # Vanna = -n(d1) * d2 / sigma
    return -n(d1(S, K, T, r, sigma)) * d2(S, K, T, r, sigma) / sigma


# Vomma (a.k.a. Volga) of an option
# Vomma = d(Vega)/dsigma = d^2 V / dsigma^2
# @param S: current spot price
# @param K: strike price
# @param T: time to expiration
# @param r: risk-free interest rate
# @param sigma: volatility
# @return: vomma
def vomma(S, K, T, r, sigma):
    # Validate input parameters
    validate_input_parameters(S, K, T, r, sigma)

    d1_val = d1(S, K, T, r, sigma)
    d2_val = d2(S, K, T, r, sigma)
    # Vomma = Vega * d1 * d2 / sigma, with Vega = S * n(d1) * sqrt(T)
    return S * n(d1_val) * np.sqrt(T) * d1_val * d2_val / sigma


# Charm of an option
# Charm = d(Delta)/dt = -d^2 V / (dS dT), the rate of change of Delta as time passes
# @param S: current spot price
# @param K: strike price
# @param T: time to expiration
# @param r: risk-free interest rate
# @param sigma: volatility
# @return: charm
def charm(S, K, T, r, sigma):
    # Validate input parameters
    validate_input_parameters(S, K, T, r, sigma)

    d1_val = d1(S, K, T, r, sigma)
    d2_val = d2(S, K, T, r, sigma)
    # Charm = -n(d1) * (2*r*T - d2*sigma*sqrt(T)) / (2*T*sigma*sqrt(T))
    return -n(d1_val) * (2 * r * T - d2_val * sigma * np.sqrt(T)) / (2 * T * sigma * np.sqrt(T))


# Veta of an option
# Veta = d(Vega)/dt = d^2 V / (dsigma dt), the rate of change of Vega as time passes
# @param S: current spot price
# @param K: strike price
# @param T: time to expiration
# @param r: risk-free interest rate
# @param sigma: volatility
# @return: veta
def veta(S, K, T, r, sigma):
    # Validate input parameters
    validate_input_parameters(S, K, T, r, sigma)

    d1_val = d1(S, K, T, r, sigma)
    d2_val = d2(S, K, T, r, sigma)
    # Veta = -S * n(d1) * sqrt(T) * [ (1 + d1*d2)/(2*T) - r*d1/(sigma*sqrt(T)) ]
    return -S * n(d1_val) * np.sqrt(T) * (
        (1 + d1_val * d2_val) / (2 * T) - r * d1_val / (sigma * np.sqrt(T))
    )


# Vera (a.k.a. Rhova) of an option
# Vera = d(Vega)/dr = d(Rho)/dsigma = d^2 V / (dsigma dr)
# @param S: current spot price
# @param K: strike price
# @param T: time to expiration
# @param r: risk-free interest rate
# @param sigma: volatility
# @return: vera
def vera(S, K, T, r, sigma):
    # Validate input parameters
    validate_input_parameters(S, K, T, r, sigma)

    d1_val = d1(S, K, T, r, sigma)
    d2_val = d2(S, K, T, r, sigma)
    # Vera = -K * T * e^(-rT) * n(d2) * d1 / sigma
    return -K * T * np.exp(-r * T) * n(d2_val) * d1_val / sigma
