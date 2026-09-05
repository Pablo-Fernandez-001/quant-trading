# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 23:16:51 2026

@author: pabda
"""

#import libs
import pandas as pd
import numpy as np
import yfinance as yf
from scipy.optimize import minimize

# Portfolio Optimizator
def Portfolio_Optimizator(returns: pd.DataFrame) -> dict:
    """
    Getting all the optimizated weights to find the greatest Sharpe ratio in a portfolio

    Parameters
    ----------
    returns : pd.DataFrame
        gets all asset return

    Returns
    -------
    dict
        returns all the optimization like a dictionary
    """
    
    # Calculates Annualizated Covariance Matrix
    volatilities_diagonal = np.diag(returns.std() * np.sqrt(252)) # Anualizated Volatilities in diagonal
    Sigma = volatilities_diagonal.dot(returns.corr()).dot(volatilities_diagonal) # Annualizated Covariance Matrix
    # Sigma = returns.cov() * 252 could be
    
    #Objetive funtion to maximize the Sharp ratio coeficient
    def sharpe_ratio(weights, sigma, rf, waited_returns):
        portfolio_waited_returns = waited_returns.dot(weights)
        portfolio_variance = weights.dot(sigma).dot(weights)
        
        return -(portfolio_waited_returns - rf) / np.sqrt(portfolio_variance)
    
    # Defining limits and condition to optimizing
    assets_number = len(returns.columns)
    w0 = np.ones(assets_number) / assets_number
    bnds = ((0,1) , ) * assets_number
    cons = {"type":"eq","fun":lambda w: np.sum(w)-1}
    
    # Free risk and the individual waited returns
    rf = 0.03
    waited_returns = returns.mean() * 252
    
    # Optimization to find the max shapre ratio portfolio
    max_sr = minimize(sharpe_ratio, w0, args=(Sigma, rf, waited_returns), constraints = cons, bounds = bnds)
    
    # Show the result of the portfolio with the greatest Sharpe Ratio Coeficient
    optimizated_weight_sr = max_sr.x
    optimizated_portfolio_returns_sr = (returns * optimizated_weight_sr).sum(axis=1).mean() * 252
    optimizated_volatility_sr_portfolio = np.sqrt(np.dot(optimizated_weight_sr, np.dot(returns.cov(), optimizated_weight_sr))) * np.sqrt(252)
    optimizated_portfolio_sharp_ratio = (optimizated_portfolio_returns_sr - rf) / optimizated_volatility_sr_portfolio
    
    return {
        "weights": optimizated_weight_sr,
        "returns" : optimizated_portfolio_returns_sr,
        "volatility": optimizated_volatility_sr_portfolio,
        "sharp ratio": optimizated_portfolio_sharp_ratio
        }

# Mergin Sharp Ratio with Magic Formula to optimize better the results
# Example (Returns)
if __name__ == "__main__":
    #Selecting assets
    file_mf = "MagicFormula.csv"
    df_mf = pd.read_csv(file_mf, index_col="Ticker")
    # Keeping the first 25 to optimize
    df_mf = df_mf.iloc[:25]
    # Getting the Historical data
    tickers = list(df_mf.index)
    start = "2023-01-01"
    end = "2024-01-01"
    df_data = yf.download(tickers, start, end, interval="1d")["Close"][list(df_mf.index)]
    #Returns
    returns = df_data.pct_change().dropna()
    
    #Portfolio Optimization
    optimization = Portfolio_Optimizator(returns)
    
    #console printing
    print(optimization)