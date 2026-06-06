from scipy.stats import norm

# Cumulative distribution function of the standard normal distribution
# @param x: value
# @return: cumulative distribution function of the standard normal distribution
def N(x):
    return norm.cdf(x)


# Probability density function of the standard normal distribution
# @param x: value
# @return: probability density function of the standard normal distribution
def n(x):
    return norm.pdf(x)


# Percentile point function of the standard normal distribution
# @param x: value
# @return: percentile point function of the standard normal distribution
def ppf(x):
    return norm.ppf(x)
