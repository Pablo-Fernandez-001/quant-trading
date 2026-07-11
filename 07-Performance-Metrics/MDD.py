# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 01:04:40 2026

@author: pabda
"""

#Maximum Drawdown
#import libs
import pandas as pd

#Hist data
df = pd.read_csv("../data/NVDA.csv", index_col="Date")
print(f"Start date: {df.index[0]}")
print(f"End date: {df.index[-1]}")


#MDD
def MDD(data: pd.DataFrame(), column: str = "Close") -> float:
    """
    It measures the worst loss suffered by an investment, allowing investors to assess the risk.

    Parameters
    ----------
    data : pd.DataFrame
        Historical data
    column : str, optional
        Used to calculate. The default is "Close".

    Returns
    -------
    float
        MDD
    """
    
    #Calculate
    daily_performance = data[column].pct_change()
    acumulated_performance = (1 + daily_performance).cumprod()
    max_acumulated_performance =  acumulated_performance.cummax()
    difference = max_acumulated_performance - acumulated_performance
    percent_difference = difference / max_acumulated_performance
    mdd = percent_difference.max()
    
    return mdd

mdd = MDD(df)
print(f"The greatest loss we could have experienced would have been: {round(mdd * 100,3)}%")

# Reminder:
#   - Maximum drawdown offers a direct view of the maximum loss we could have experienced on an investment.
#   - Maximum drawdown helps us manage risk in our portfolios more effectively.