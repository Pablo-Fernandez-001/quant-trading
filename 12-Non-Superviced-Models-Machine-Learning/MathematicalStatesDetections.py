# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 19:13:00 2026

@author: pabda
"""

# Sometimes the bullish trend gets 0 value or 1 value when you refresh the data, and we going to 
# normalize the data to have uniform values to bullish or bearish trend

# Import libraries
import numpy as np
import yfinance as yf
from hmmlearn import hmm
import matplotlib.pyplot as plt

# Get data
start="2021-01-01"
end="2024-01-01"
ticker="SPY"
df = yf.download(ticker, start, end, interval="1d")

# Add logarithmic returns and the daily range of each candle
df["log_r"] = np.log(df["Close"] / df["Close"].shift(periods=1))
df["range"] = df["High"].div(df["Low"]) - 1

# Define the model with 2 hidden states
model = hmm.GaussianHMM(n_components=2, covariance_type="full", random_state=1)

# Fit the model
data = df[["log_r", "range"]].dropna()
model.fit(data)

# Predict
hidden_states = model.predict(data)

# Separate Hidden States
Close = df.loc[data.index, "Close"].squeeze()
state0 = Close.where(hidden_states==0, np.nan)
state1 = Close.where(hidden_states==1, np.nan)

n_continuity = 25
states = {"Bullish":None,"Bearish":None}

# Iterates over the rows from whatever state (state0 and state1)
for i in range(state0.shape[0] - n_continuity):
    substate0 = state0.iloc[i:i + n_continuity].dropna() # we delete the NAN values for continuity, we filled up all empty data from the trend
    # with NAN values
    
    # Review if we have 25 continuous data
    if substate0.shape[0] == n_continuity:
        
        # Fit Regression to know the slope
        params = np.polyfit(
            x=range(0, n_continuity),
            y=substate0,
            deg=1
        )
        
        slope = params[0]
        
        if slope > 0:
            states["Bullish"] = state0
            states["Bearish"] = state1
        else:
            states["Bullish"] = state1
            states["Bearish"] = state0
            
        # Cease execution
        break

# Visualize
plt.figure(figsize=(22,12))

plt.plot(states["Bearish"], color="red", label="Bearish trend")
plt.plot(states["Bullish"], color="green", label="Bullish trend")

plt.title("Hidden States into the ETF (SPY)- Bullish/Bearish")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()

# Reminder:
#   - Our model's internal states can be detected from the sign of the slope of the fitted regression.