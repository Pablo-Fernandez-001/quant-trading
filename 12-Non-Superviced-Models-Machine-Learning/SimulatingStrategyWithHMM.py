# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 23:16:56 2026

@author: pabda
"""

#import libs
import pandas as pd
import numpy as np
import yfinance as yf
from hmmlearn import hmm
import matplotlib.pyplot as plt


# Get historical data
df = yf.download("SPY", start="2019-01-01", end="2024-01-01", interval="1d")

# Create columns for the model (logarithmic returns and range)
df["log_r"] = np.log(df["Close"] / df["Close"].shift(periods=1))
df["range"] = df["High"] / df["Low"] - 1
df = df.dropna()

# Separate training and testing data
x_train = df[["log_r", "range"]].loc[:"2021-12-31"] # First 3 years of data
x_test = df[["log_r", "range"]].loc["2022-01-01":] # Next 2 years to validate the model

print(f"Training data length: {x_train.shape[0]} - from {x_train.index[0]} to {x_train.index[-1]}")
print(f"Testing data length: {x_test.shape[0]} - from {x_test.index[0]} to {x_test.index[-1]}")

# Define and fit the model with 2 states (bullish and bearish)
model = hmm.GaussianHMM(n_components=2, covariance_type="full", random_state=1)
model.fit(x_train)

# Predict training and testing data
hidden_states_training = model.predict(x_train)
hidden_states_testing = model.predict(x_test)

# Compare returns of each investment method with testing data:
#   1. Strategy 1: Buy and Hold
#   2. Strategy 2: Moving Average Crossover
#   3. Strategy 3: Invest based on the Markov Model prediction

# Testing data
df_testing = df.loc[x_test.index].copy()

# Convert Close into a one-dimensional Series
close = df_testing["Close"].squeeze()


# Strategy 1: Buy and Hold
df_testing["strategy1_return"] = (close.pct_change() + 1).cumprod()


# Strategy 2: Moving Average Crossover
ma_9d = close.rolling(window=9).mean()
ma_21d = close.rolling(window=21).mean()

# Detect crossovers
crossover = np.where(ma_9d > ma_21d, 1, -1)

# Fill crossover nans forward
crossover = pd.Series(crossover, index=df_testing.index).ffill()

# Calculate return
daily_returns = close.pct_change()

df_testing["strategy2_return"] = (
    1 + crossover.shift(periods=1) * daily_returns
).cumprod()


# Strategy 3: Invest Based on the Markov Model Prediction
state0 = close.where(hidden_states_testing == 0, np.nan)
state1 = close.where(hidden_states_testing == 1, np.nan)

n_continuity = 25
states = {"bullish": None, "bearish": None}

# Iterate over the rows of any state (state0 or state1)
for i in range(state0.shape[0] - n_continuity):

    sub_state0 = state0.iloc[i:i + n_continuity].dropna()

    # Check if there are 25 continuous data points
    if sub_state0.shape[0] == n_continuity:

        # Fit Regression to determine the slope
        params = np.polyfit(
            x=range(0, n_continuity),
            y=sub_state0,
            deg=1
        )

        slope = params[0]

        if slope > 0:
            states["bullish"] = state0
            states["bearish"] = state1
        else:
            states["bullish"] = state1
            states["bearish"] = state0

        # Cease execution
        break


# If no 25 continuous observations were found in state0,
# determine bullish and bearish states using average logarithmic returns
if states["bullish"] is None:

    state0_return = x_test.loc[
        hidden_states_testing == 0,
        "log_r"
    ].mean()

    state1_return = x_test.loc[
        hidden_states_testing == 1,
        "log_r"
    ].mean()

    if state0_return > state1_return:
        states["bullish"] = state0
        states["bearish"] = state1
    else:
        states["bullish"] = state1
        states["bearish"] = state0


# Visualize
plt.figure(figsize=(22, 12))

plt.plot(
    states["bearish"],
    color="red",
    label="Bearish Trend"
)

plt.plot(
    states["bullish"],
    color="green",
    label="Bullish Trend"
)

plt.title("Hidden States in the ETF (SPY) - Bullish/Bearish")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()


# Get direction and return
direction = np.where(
    states["bullish"].notnull(),
    1,
    -1
)

direction = pd.Series(
    direction,
    index=df_testing.index,
    name="Direction"
)

df_testing["strategy3_return"] = (
    1 + direction.shift(periods=1) * daily_returns
).cumprod()


# Plot returns for the strategies
df_testing[
    [
        "strategy1_return",
        "strategy2_return",
        "strategy3_return"
    ]
].plot(figsize=(22, 12))

plt.title("Return Comparison for Strategies")
plt.xlabel("Time")
plt.ylabel("Capital Behavior")
plt.legend()
plt.grid()
plt.show()


# Reminders:
#   - The internal states of the Markov model help us detect the current trends of financial assets.
#   - The fact that the model adapts well to one financial instrument does not mean that it will work for another.
#   - We can fit the Markov model to an index (as we did in this lesson) to make more informed decisions,
#     since most stocks are highly correlated with indices. For example, if the Markov model
#     does not fit a stock that has a high correlation with the S&P 500, such as Microsoft (MSFT), but through
#     another model (perhaps technical indicators) we detect a bullish trend, then we could combine both analyses to
#     improve the accuracy of our investments.