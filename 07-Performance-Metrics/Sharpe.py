# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 20:39:05 2026

@author: pabda
"""

# import libs
import pandas as pd
import numpy as np

#get data
df = pd.read_csv("../data/AMZN.csv", index_col="Date")
print(f"Start date: {df.index[0]}")
print(f"End date: {df.index[-1]}")

#Sharpe
def sharpe_ratio(data: pd.DataFrame, fr_ratio: float = 0.03, column: str = "Close") -> float:
    """
    This function makes the Sharpe's ratio for each invertion's asset risk unit assumed

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
        Sharpe ratio
    """
    
    #Calculate
    asset_return = ((data[column][-1]/data[column][0]) ** (1/np.ceil(data.shape[0]/252))) - 1
    annualizated_std = data[column].pct_change().std() * np.sqrt(252)
    
    return (asset_return - fr_ratio) / annualizated_std

#Testing
sr = sharpe_ratio(df, fr_ratio=0.03, column="Close")
print(f"Sharpe ratio {sr}", end="\n"*2) # that "end="\n"*2" means 2 new lines


if sr > 0:
    print(f"""
          This inversion generates a superior free risk ratio, assuming the assumed risk
          it's a good adjusted risk ratio.
          Sharpe ratio getted: {sr}.
          """)
else:
    print(f"""
          This inverssion generates losses compared with a free risk asset inversion.
          In this case, it's convenient to invest more in free risk assets like secure bank witdrawals,
          goverment bonds, or theasure bonds.
          Sharpe ratio getted: {sr}
          """)

# Reminder:
#   - The Sharpe Ratio represents the return an investment offers for each unit of risk assumed.
#   - A positive value indicates a return exceeding the risk-free rate, relative to the risk taken.
#   - A negative value suggests it is better to invest in risk-free assets.