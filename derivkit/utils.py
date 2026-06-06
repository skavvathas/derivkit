from scipy.stats import norm

# Validate input parameters for scalar
# @param x: value
# @return: True if input parameters are valid, False otherwise
def validate_input_parameters_scalar(x):
    if np.any(np.isnan(x)):
        raise ValueError("x must not contain NaN")
    if np.any(np.isinf(x)):
        raise ValueError("x must not contain infinity")
    if x.ndim != 0:
        raise ValueError("x must be a scalar")
    if x.size != 1:
        raise ValueError("x must be a scalar")
    return True

# Cumulative distribution function of the standard normal distribution
# @param x: value
# @return: cumulative distribution function of the standard normal distribution
def N(x):
    validate_input_parameters_scalar(x)
    return norm.cdf(x)


# Probability density function of the standard normal distribution
# @param x: value
# @return: probability density function of the standard normal distribution
def n(x):
    validate_input_parameters_scalar(x)
    return norm.pdf(x)


# Percentile point function of the standard normal distribution
# @param x: value
# @return: percentile point function of the standard normal distribution
def ppf(x):
    validate_input_parameters_scalar(x)
    return norm.ppf(x)


# Validate input parameters
# @param S: current spot price
# @param K: strike price
# @param T: time to expiration
# @param r: risk-free interest rate
# @param sigma: volatility
# @param option_type: 'call' or 'put'
# @return: True if input parameters are valid, False otherwise
def validate_input_parameters(S, K, T, r, sigma, option_type='call'):
    if option_type not in ['call', 'put']:
        raise ValueError("option_type must be 'call' or 'put'")
    if T <= 0:
        raise ValueError("T must be greater than 0")
    if r < 0:
        raise ValueError("r must be greater than 0")
    if sigma <= 0:
        raise ValueError("sigma must be greater than 0")
    if S <= 0:
        raise ValueError("S must be greater than 0")
    if K <= 0:
        raise ValueError("K must be greater than 0")
    return True


# Validate input parameters for risk metrics
def validate_input_parameters_risk_metrics(prices):
    if not isinstance(prices, np.ndarray):
        raise ValueError("prices must be a numpy array")
    if prices.ndim != 1:
        raise ValueError("prices must be a 1D numpy array")
    if prices.size == 0:
        raise ValueError("prices must not be empty")
    if np.any(prices <= 0):
        raise ValueError("prices must be positive")
    if np.any(np.isnan(prices)):
        raise ValueError("prices must not contain NaN")
    if np.any(np.isinf(prices)):
        raise ValueError("prices must not contain infinity")