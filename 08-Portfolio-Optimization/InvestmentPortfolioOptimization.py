# -*- coding: utf-8 -*-

"""
Created on Thu Aug  6 21:29:53 2026

@author: pabda
"""

# 15000 portfolios to search which one is the best
# import libs
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

# getting close's prices
assets = ["AAPL", "MSFT", "GOOGL", "DIS"]
start_date = "2023-01-01"
end_date = "2024-01-01"

prices = yf.download(
    tickers=assets,
    start=start_date,
    end=end_date,
    interval="1d"
)

# sorting
prices = prices["Close"][assets]

# returns
returns = prices.pct_change().dropna()

# getting assets correlation
correlation = returns.corr()
plt.figure(figsize=(22, 12), dpi=100)
sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)
plt.title("Returns' Correlation Matrix")
plt.show()

#### To test

print(prices.head())
print(prices.tail())

print("\nPrices shape:")
print(prices.shape)

print("\nNaN per asset:")
print(prices.isna().sum())

print("\nReturns shape:")
print(returns.shape)

print("\nCorrelation:")
print(correlation)

# End tests

# covariance
covariance = returns.cov()

# Portfolio weights for each asset
weights = np.array([0.33,0.33,0.33,0.01])

# Annualizated portfolio returns
portfolio_returns = (returns * weights).sum(axis=1).mean() * 252
print(f"Annualizated portfolio returns of the waited inversion {portfolio_returns}")

# Annualizated Portafolio Volatility
portfolio_volatility = np.sqrt(np.dot(weights, np.dot(covariance, weights))) * np.sqrt(252)
print(f"Annualizated portfolio volatility of the waited inversion {portfolio_volatility}")

#create portfolios (15000 different protfolio)
portfolios_numbers = 15_000

#load results in an array(returns, volatilty, sharpe-ratio)
results = np.zeros((3, portfolios_numbers))
weights_list = []

#Iterate to create each portfolio
for i in range(portfolios_numbers):

    #Choose random weights
    weights = np.random.random(4)

    #rebalancing the weights so that they add up to one
    weights = weights / np.sum(weights)

    #Calculate returns and volatility about the price
    portfolio_returns = (returns * weights).sum(axis=1).mean()*252
    portfolio_volatility = np.sqrt(np.dot(weights, np.dot(covariance, weights))) * np.sqrt(252)

    #Load data
    results[0,i] = portfolio_returns
    results[1,i] = portfolio_volatility
    results[2,i] = (portfolio_returns - 0.03) / portfolio_volatility # Sharp ratio
    weights_list.append(weights)


#Convert data into a dataframe
results = pd.DataFrame(
    results.T,
    columns=["Annual Return", "Annual Volatility", "Sharpe-Ratio"]
)

#Plotting
plt.figure(figsize=(22,12))

plt.scatter(
    results["Annual Volatility"],
    results["Annual Return"],
    c=results["Sharpe-Ratio"],
    cmap="RdYlBu",
    edgecolors="black",
    linewidths=0.45,
    s=50
)

plt.title("Waited Return vs Volatility", size=25)
plt.xlabel("Volatility $\sigma$", size=25)
plt.ylabel("Annual Returns $E[r]$", size=25)
plt.colorbar()
plt.tight_layout()
plt.show()


#Parte 2
#Find the minimum variance portfolio
min_volatility_portfolio = results.loc[results["Annual Volatility"].idxmin()]

portfolio_weights = list(
    zip(
        assets,
        weights_list[results["Annual Volatility"].idxmin()]
    )
)

print(
    f"Minimumn Variance Portfolio: \n"
    f"{min_volatility_portfolio}, \n"
    f"The portfolio weights are: \n"
    f"{portfolio_weights}"
)


#Find the max sharpe portfolio ratio
max_sharpe_portfolio = results.loc[results["Sharpe-Ratio"].idxmax()]

portfolio_sharpe_weights = list(
    zip(
        assets,
        weights_list[results["Sharpe-Ratio"].idxmax()]
    )
)

print(
    f"Max Sharpe Ratio portfolio \n"
    f"{max_sharpe_portfolio}, \n"
    f"The portfolio sharpe ratio weights are\n"
    f"{portfolio_sharpe_weights}"
)


#Plotting portfolios
plt.figure(figsize=(22,12))
plt.scatter(
    results["Annual Volatility"],
    results["Annual Return"],
    c=results["Sharpe-Ratio"],
    cmap="RdYlBu",
    edgecolors="black",
    linewidths=0.45,
    s=50
)

plt.colorbar()
#to show the minimum variance portfolio into the same plot
plt.scatter(
    min_volatility_portfolio["Annual Volatility"],
    min_volatility_portfolio["Annual Return"],
    marker="X",
    color="r",
    s=500,
    edgecolors="black",
    lw=3,
    label="Minnimum Variance Portfolio"
)

#to show the maximum sharpe ratio portfolio into the same plot
plt.scatter(
    max_sharpe_portfolio["Annual Volatility"],
    max_sharpe_portfolio["Annual Return"],
    marker="X",
    color="yellow",
    s=500,
    edgecolors="black",
    lw=3,
    label="Maximum Sharpe Ratio Portfolio"
)

plt.title("Waited Return vs Volatility", size=25)
plt.xlabel("Volatility $\sigma$", size=25)
plt.ylabel("Annual Returns $E[r]$", size=25)
plt.legend()
plt.tight_layout()
plt.show()


# Part 3, finding with optimization the perfect weights, and another things
## Optimizations
# Calculating the Annualizated Covariance Matrix
volatilities_diagonal = np.diag(
    returns.std() * np.sqrt(252)
) # Annualizated Volatilities diagonal

Sigma = volatilities_diagonal.dot(
    correlation
).dot(
    volatilities_diagonal
) # Annualizated Covariance Matrix
# Sigma = returns.cov() * 252 <- this it's the easy way to get sigma, the up-side code it's the precise way


#Target function to minimize the portfolio variance
def variance(weights,sigma):
    return weights.dot(Sigma).dot(weights)


#Define the limits and condition to optimize the minimum variance
asets_numbers = len(assets)
w0 = np.ones(asets_numbers) / asets_numbers # initial weights
bnds = ((0,1),) * asets_numbers # The max weight must be between into 0 and 1, and that variable it's the limits
cons = {
    "type":"eq",
    "fun": lambda w: np.sum(w) - 1
}

# Optimize to find the minimum portfolio variance
minvar = minimize(
    variance,
    w0,
    args=(Sigma,),
    bounds=bnds,
    constraints=cons
)

# Showing each results of minimum portfolio variance
optimizated_weights = minvar.x
return_optimizated_portfolio = (
    returns * optimizated_weights
).sum(axis=1).mean() * 252

volatility_optimizated_portfolio = np.sqrt(
    np.dot(
        optimizated_weights,
        np.dot(covariance, optimizated_weights)
    )
) * np.sqrt(252)

annual_min_portfolio = min_volatility_portfolio["Annual Return"]
annual_min_volatility_portfolio = min_volatility_portfolio["Annual Volatility"]

print(
    f"Before Better Minimum Variance Portfolio "
    f"\n Return: {annual_min_portfolio} "
    f"\nVolatility: {annual_min_volatility_portfolio}"
)

print("-----"*20)

print(
    f"Current Better Minimum Variance Portfolio "
    f"\n Return: {return_optimizated_portfolio}, "
    f"\nVolatility: {volatility_optimizated_portfolio}"
)


#Target Sharpe Ratio's function
def sharpe_ratio(weights, sigma, rf, waited_returns):
    waited_portfolio_retunrs = waited_returns.dot(weights)
    portfolio_variance = weights.dot(sigma).dot(weights)
    return -(waited_portfolio_retunrs - rf ) / np.sqrt(portfolio_variance) # It's the same like others, just the "-" sign means the greater result than the function could find

#Define the limits and condition to optimize the minimum variance
asets_numbers = len(assets)
w0 = np.ones(asets_numbers) / asets_numbers # initial weights
bnds = ((0,1),) * asets_numbers # The max weight must be between into 0 and 1, and that variable it's the limits
cons = {
    "type":"eq",
    "fun": lambda w: np.sum(w) - 1
}

#Define risk-free rate and the waited individual returns
rf = 0.03
waited_returns = returns.mean() * 252 # we wait the optimization here

#Optimize to find the maximum Sharpe Ratio portfolio
max_sr = minimize(
    sharpe_ratio,
    w0,
    args=(Sigma, rf, waited_returns),
    bounds=bnds,
    constraints=cons
)


# Showing each result of the maximum Sharpe Ratio portfolio
optimized_weights_sr = max_sr.x
return_optimized_portfolio_sr = (
    returns * optimized_weights_sr
).sum(axis=1).mean() * 252
volatility_optimized_portfolio_sr = np.sqrt(
    np.dot(
        optimized_weights_sr,
        np.dot(covariance, optimized_weights_sr)
    )
) * np.sqrt(252)
annual_max_sharpe_portfolio = max_sharpe_portfolio["Annual Return"]
annual_max_sharpe_volatility_portfolio = max_sharpe_portfolio["Annual Volatility"]
print("-----"*20)
print(
    f"Previous Best Maximum Sharpe Ratio Portfolio "
    f"\nReturn: {annual_max_sharpe_portfolio} "
    f"\nVolatility: {annual_max_sharpe_volatility_portfolio}"
)
print("-----"*20)
print(
    f"Current Best Maximum Sharpe Ratio Portfolio "
    f"\nReturn: {return_optimized_portfolio_sr} "
    f"\nVolatility: {volatility_optimized_portfolio_sr}"
)

# Reminder:
# - The Minimum Variance Portfolio is the one that offers the lowest possible volatility for a given level of
# expected return, making it ideal for investors seeking to minimize risk.
# - On the other hand, the portfolio with the highest Sharpe ratio represents the optimal combination of risk and return,
# making it the preferred choice for investors seeking to maximize risk-adjusted returns.