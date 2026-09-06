# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 00:43:05 2026

@author: pabda
"""

#import libs
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
# Own libraries
from Fundamental import Magic_Formula
from PortfolioOptimization import Portfolio_Optimizator

#Defining Long Term Trading/Investmen or Position Trader System
def Position_System() -> None:
    """
    Runs a long-term position trading and investment system based on fundamental screening
    and portfolio optimization.
    
    The system selects the 30 largest companies in the S&P 500 by market capitalization,
    applies the Magic Formula to rank the selected assets, and uses the resulting tickers
    to download one year of daily historical market data.
    
    The historical returns are then used to optimize the portfolio allocation by maximizing
    the Sharpe ratio. Finally, the system displays the optimized asset weights together with
    the expected portfolio return, volatility, and Sharpe ratio.
    
    Returns
    -------
    None
        The optimized portfolio weights and performance metrics are printed to the console.
    """
    
    # Geting Actives
    tickers = pd.read_csv(("S&P 500.csv")).sort_values(by="marketCap", ascending=False)["Symbol"].tolist()[:30]
    #Magic Formula
    mf = Magic_Formula(tickers)
    #Dates and tickers
    mf_tickers = list(mf.index)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365) #Last year
    # Formatting
    end_date = end_date.strftime("%Y-%m-%d")
    start_date = start_date.strftime("%Y-%m-%d")
    
    df_tickers = yf.download(mf_tickers, start_date, end_date, interval="1d", progress=False)["Close"]
    #Sorting the downloads into the initial/original order
    df_tickers = df_tickers[mf_tickers]
    #Returns
    returns = df_tickers.pct_change().dropna()
    #Portfolio Optimizing
    optimization = Portfolio_Optimizator(returns)
    # print information
    ponderations = list(zip(returns.columns, optimization["weights"]))
    sorted_ponderations = sorted(ponderations, key= lambda x: x[1])[::-1] # ::-1 to go through the entire list
    optimizated_returns = optimization["returns"]
    portfolio_volatility = optimization["volatility"]
    sharpe_ratio_portfolio = optimization["sharpe ratio"]
    print(f"""Portfolio Ponderations {sorted_ponderations}, \n
          Portfolio Returns {optimizated_returns}, \n
          Portfolio Volatility: {portfolio_volatility}, \n
          Sharpe Ratio: {sharpe_ratio_portfolio}""")

# Example (reminder)
if __name__ == "__main__":
    # Excecuting System
    Position_System()