import numpy as np
from utils import ppf

# Max Drawdown of a price series
# @param prices: numpy array of prices
# @return: numpy array of drawdowns
def max_drawdown(prices):
    prices = np.asarray(prices, dtype=float)
    peak = np.maximum.accumulate(prices)
    drawdowns = (prices - peak) / peak
    return drawdowns.min()


# Sharpe ratio of a returns series
# @param returns: numpy array of returns
# @param rf: risk-free rate
# @return: Sharpe ratio
def sharpe_ratio(returns, rf=0.0, periods=252):
    std = returns.std()
    risk_free_rate = rf
    annualized_returns = returns.mean() * periods
    annualized_std = std * np.sqrt(periods)
    return (annualized_returns - risk_free_rate) / annualized_std

# Sortino ratio of a returns series
# @param returns: numpy array of returns
# @param rf: risk-free rate
# @param periods: number of periods in a year
# @return: Sortino ratio
def sortino_ratio(returns, rf=0.0, periods=252):
    downside_std = returns[returns < 0].std()
    risk_free_rate = rf
    annualized_returns = returns.mean() * periods
    annualized_downside_std = downside_std * np.sqrt(periods)
    return (annualized_returns - risk_free_rate) / annualized_downside_std

# Realized volatility of a price series
# @param prices: numpy array of prices
# @param window: window size for the realized volatility
# @return: numpy array of realized volatility
def realized_volatility(prices, window=20):
    prices = np.asarray(prices, dtype=float)
    log_returns = np.log(prices[1:] / prices[:-1])
    if len(log_returns) < window:
        return np.nan
    vol = np.array([
        log_returns[i - window:i].std() * np.sqrt(252)
        for i in range(window, len(log_returns) + 1)
    ])
    return vol

# Parametric Value at Risk
# @param returns: numpy array of returns
# @param confidence: confidence level for the VaR
# @return: numpy array of VaRs
def parametric_var(returns, confidence=0.95):
    mu = returns.mean() 
    sigma = returns.std()
    z = ppf(confidence)
    var_pct = -(mu - z * sigma)
    return var_pct