from scipy.stats import norm

# Cumulative distribution function of the standard normal
def N(x):
    return norm.cdf(x)

# Probability density function of the standard normal
def n(x):
    return norm.pdf(x)
