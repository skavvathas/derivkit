import numpy as np

# Max drawdown metric is the maximum percentage loss from a peak to a trough in a price series
def max_drawdown(prices):
    prices = np.asarray(prices, dtype=float)
    peak = np.maximum.accumulate(prices)
    drawdowns = (prices - peak) / peak
    return drawdowns.min()
