# -*- coding: utf-8 -*-

"""
Created on Tue Aug 11 17:47:20 2026

@author: pabda
"""

#import libs
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt

#Nadaraya-Watson's Estimator/Envelope
def Estimator_Nadaraya_Watson_Envelope(df: pd.DataFrame, length: int = 500, band_width: float = 8.0, factor: float = 3.0, column: str = "Close") -> pd.DataFrame:
    """
    The Nadaraya-Watson Estimator can be described as a series of weighted averages using a specific normalized kernel
    as the weighting function. For each point of the estimator at time t, the peak of the kernel is located at time t, so
    the highest weights are assigned to price values neighboring the price at time t.

    A lower bandwidth value would contribute toward a more significant weighting of the price at a precise point, and as such,
    would produce less smoothed results. However, when the bandwidth is sufficiently large, prices would be weighted
    similarly, resulting in an output closer to the mean price.

    It is interesting to note that due to the nature of the estimator and its weighting procedure, real-time results
    would not deviate drastically for points in the estimator near the center of the calculation window.

    The Nadaraya-Watson Envelope highlights the extremes reached by prices within the selected window size. This is achieved
    by estimating the underlying price trend through kernel smoothing, calculating the mean absolute deviations from it, and
    adding/subtracting them from the estimated underlying trend.

    How to Trade It:
        
        The price is expected to reverse when it crosses one of the envelope boundaries or when a new reversal point is
        reached in the NW Estimator.
        
    Parameters
    ----------
    param : pd.DataFrame : df : Historical asset data.
    ----------
    param : int : length : Determines the number of recent price observations that will be used to fit the
                           Nadaraya-Watson Estimator (by default, it is set to 500).
    ----------
    param : float : band_width : Controls the degree of smoothness of the envelopes, with higher values returning smoother
                                 results (by default, it is set to 8.0).
    ----------
    param : float : factor : Controls the width of the envelope (by default, it is set to 3.0).
    ----------
    param : str : column : Column to use in the NW Est/Env calculation (by default, it is set to "Close").

    Returns:
    ----------
    return : pd.DataFrame : Nadaraya-Watson Estimator/Envelope calculation.
    """

    #Calculate
    assert df.shape[0] >= length, "The length of the DataFrame (df) must be greater than or equal to (>=) the length"
    column_price = df[-length:][column]
    rows = np.arange(0, length)
    weights_matrix = np.array( np.exp( -np.power((np.matrix(rows).T - np.matrix(rows)), 2 ) / ((band_width ** 2) * 2 )))
    x_sum = (weights_matrix * np.tile(column_price.values, (length, 1))).sum(axis=1)
    y2 = x_sum / weights_matrix.sum(axis=1)
    nwee = pd.DataFrame(data=y2, index=column_price.index, columns=["Estimator"]) #Nadaraya-Watson Estimator Envelope

    #Estimator Direction
    d = nwee["Estimator"] - nwee["Estimator"].shift(periods=1)
    d_s = d.shift(periods=1)
    nwee["Estimator Direction"] = np.where((d > 0) & (d_s < 0), 1, np.where((d < 0) & (d_s > 0), -1, np.nan))
    nwee["Estimator Direction"] = nwee["Estimator Direction"].shift(periods=-1)

    #Upper and Lower Bands Direction
    mae = (column_price - y2).abs().mean() * factor
    nwee["Upper Band"] = y2 + mae
    nwee["Lower Band"] = y2 - mae
    s_column_price = column_price.shift(periods=1)
    bands_direction = np.where(((s_column_price < (y2 - mae))) & ((column_price > (y2 - mae))), 1, np.where(((s_column_price > (y2 + mae))) & ((column_price < (y2 + mae))), -1, np.nan))
    nwee["Bands Direction"] = bands_direction
    nwee["Bands Direction"] = nwee["Bands Direction"].shift(periods=-1)

    return nwee


# Getting data

file_path = "../data/AMZN.csv"
df = pd.read_csv(file_path, index_col = "Date", parse_dates=True)

# Calculates indicator
nw = Estimator_Nadaraya_Watson_Envelope(df)

# Estimator Direction
nw_positive_estimator = nw["Estimator"].where(nw["Estimator Direction"].ffill() >= 0, np.nan) # ffill == forward fill
nw_negative_estimator = nw["Estimator"].where(nw["Estimator Direction"].ffill() < 0, np.nan)

# Plotting
nw_plots = [
mpf.make_addplot(nw_positive_estimator, label ="Positive Estimator", color="green"),
mpf.make_addplot(nw_negative_estimator, label ="Negative Estimator", color="red"),
mpf.make_addplot(nw["Upper Band"], label ="Upper Band", color="green"),
mpf.make_addplot(nw["Lower Band"], label ="Lower Band", color="red"),
]

mpf.plot(df[-500:], type="candle", style="yahoo", volume=True, figsize=(22,10), addplot=nw_plots, figscale=3.0, title = "Nadaraya-Watson Estimator And Envelope")
plt.show()

# Reminder:

# - The adaptability of our Nadaraya-Watson EE indicator allows us to capture trends and price extremes, providing
# a dynamic view of the market.
# - It is important to consider the indicator's daily recalculation, as this can lead to instability in the generated signals.