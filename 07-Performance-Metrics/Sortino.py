# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 22:53:01 2026

@author: pabda
"""

#Import libs
import pandas as pd
import numpy as np

#Hist data
df = pd.read_csv("../data/MSFT.csv", index_col="Date")
print(f"Start date: {df.index[0]}")
print(f"End date: {df.index[-1]}")

#Sortino ratio
def sortino_ratio(data: pd.DataFrame, fr_ratio: float = 0.03, column: str = "Close") -> float:
    """
    This function makes the Shortino's ratio for each invertion's asset risk unit assumed.
    It measures risk-adjusted performance by considering only downside volatility, making it
    more sensitive to losses than the Sharpe ratio.

    Parameters
    ----------
    data : pd.DataFrame
        Historical data from an asset
    fr_ratio : float, optional
        Free Risk ratio. The default is 0.03.
    column : str, optional
        Used to calculate. The default is "Close".

    Returns
    -------
    float
        Sortino's ratio
    """
    
    # Calculate
    active_performance = ((data[column][-1]/data[column][0]) ** (1/np.ceil(data.shape[0]/252))) - 1
    daily_performance = data[column].pct_change()
    negative_daily_performance = daily_performance[daily_performance < 0]
    negative_std = negative_daily_performance.std() * np.sqrt(252)
    
    return (active_performance - fr_ratio) / negative_std

sr = sortino_ratio(df)
print(f"Sortino Ratio: {sr}")
if sr > 0:
    print(f"""
          The investment's return exceeds the target rate of return when considering only
          downside volatility or unwanted losses.
          Sortino's ratio getted: {sr}
          """)
else:
    print(f"""
          The investment's return falls short of the target rate of return when considering only
          downside volatility or unwanted losses.
          Sortino's ratio getted: {sr}
          """)
          
# Reminder:
#   - The Sharpe ratio evaluates risk-adjusted return based on total volatility, whereas the Sortino ratio
#     focuses on downside volatility, improving accuracy by penalizing only unwanted losses.