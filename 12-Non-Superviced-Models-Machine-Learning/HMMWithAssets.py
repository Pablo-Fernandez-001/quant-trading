# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 22:44:42 2026

@author: pabda
"""

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

# Visualize
plt.figure(figsize=(22, 12))
plt.plot(state0, color="green", label="Bullish Trend")
plt.plot(state1, color="red", label="Bearish Trend")
plt.title("Hidden States in the ETF (SPY) - Bullish/Bearish")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()

# Reminder:
#   - To detect market trends with the HMM model, we must adapt the data to provide the information
#     required by the model.
#   - The white spaces mean an overlap with the dataframes and data.