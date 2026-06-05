import numpy as np


def max_drawdown(prices):
    prices = np.asarray(prices, dtype=float)
    peak = np.maximum.accumulate(prices)
    drawdowns = (prices - peak) / peak
    return drawdowns.min()


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
