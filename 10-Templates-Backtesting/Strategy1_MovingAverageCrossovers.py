# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 00:31:05 2026

@author: pabda
"""

# Standard Libraries
...
import pandas as pd
import numpy as np
import yfinance as yf
import time
import mplfinance as mpf

# Custom Libraries
...


# Strategy Class
class Strategy1:
    
    """ 
    Strategy 1: Moving Average Crossover
    
        Description:
            
            A strategy that uses moving average crossovers to identify buy and sell signals.
    
    Strategy For:
        
        - Stocks
        - Indices
        - ETFs
        - Currencies
        - Commodities
        - Cryptocurrencies
        
    Timeframes:
        
        - Daily
        - Weekly
        - Monthly
        
    Holding Period:
        
        - Variable (Depends on trend strength)
        
    Analysis Used: 
        
        - Technical Analysis
            * Moving Averages

    Detailed Strategy Description:    
        
        A strategy that seeks to capitalize on moving average crossovers as market entry and exit signals. 
        A buy is triggered when the short-term moving average crosses above the long-term moving average,
        indicating bullish momentum. A sell occurs when the crossover is reversed, signaling a potential
        trend change.
                        
        Stop Loss and Take Profit Description:
            
            Take Profit:
                
                Profit-taking is triggered when a signal opposite to the current position occurs.
                
            Stop Loss:
                
                Loss limitation occurs when a signal opposite to the current position occurs.
                
    General Assumptions:
        
        - This strategy does not account for costs or commissions (opening fees, rollovers, etc.).
        
    Notes:
        
        - Using this strategy on short timeframes (seconds, minutes, or hours) may generate many
          false signals.
    """
    
    __version__ = 1.0
    
    # __init__
    def __init__(self, df: pd.DataFrame, st_window: int = 9, lt_window: int = 21, column: str = "Close") -> None:
        
        """
        Constructor.
        
        Parameters
        ----------
        param : pd.DataFrame : df : Historical data for the financial instrument.
        ----------
        param : int : st_window : Short-term window (default is 9).
        ----------
        param : int : lt_window : Long-term window (default is 21).
        ----------
        param : str : column : Column to be used for the calculation (default is "Close").
        
        Output
        -------
        return: NoneType : None.
        """
        
        # Attributes
        self.df = df
        self.st_window = st_window
        self.lt_window = lt_window
        self.column = column
        self.strategy_calculus = None
        # Private Attributes
        
    
    # __repr__
    def __repr__(self) -> str:
        return self.__class__.__name__ + ".class"
    
    
    # Backtest
    def backtest(self) -> pd.DataFrame:
        
        """
        This method obtains the strategy's return over the entire period.
        
        Output
        ------
        return: pd.DataFrame : Strategy return over time.
        """
        
        # Calculate
        if self.strategy_calculus is None:
            self.calculate()
        
        data = self.strategy_calculus.copy()
        data["Return"] = self.df[self.column].pct_change()
        #Null deleting
        data.dropna(inplace=True)
        #Return Calculate
        returns = (1 + data["Crossover"].shift(periods=1) * data["Return"]).cumprod()
        
        return returns
    
    
    # Calculate
    def calculate(self) -> dict:
        
        """
        This method calculates the moving average crossover using historical data for a financial instrument.

        Output
        -------
        return: dict|bool : Returns a dictionary if a signal was generated on the last candle, or False if none was generated.
        """
        
        # Calculate   
        
        price = self.df[self.column]
        ma_fast = price.rolling(window=self.st_window, min_periods=self.st_window).mean() #moving average fast
        ma_fast_s = ma_fast.shift(periods=1)
        ma_slow = price.rolling(window=self.lt_window, min_periods=self.lt_window).mean() #moving average slow
        ma_slow_s = ma_slow.shift(periods=1)
        #Moving Average crossover
        crossover = np.where(((ma_fast > ma_slow) & (ma_slow_s > ma_fast_s)), 1,
                             np.where(((ma_fast < ma_slow) & (ma_slow_s < ma_fast_s)), -1, np.nan))
        #Filling Trend
        crossover = pd.Series(crossover, index=self.df.index).ffill()
        # Merged columns
        mac = pd.concat([ma_fast, ma_slow, crossover], axis=1)
        mac.columns = ["Fast Moving Average", "Slow Moving Average", "Crossover"]
        
        #Saving calculus attribute
        self.strategy_calculus = mac
        
        #Showing if we generates a signal
        if mac["Crossover"].iloc[-2] != mac["Crossover"].iloc[-1]: # Mades a trend reversal
            #Trend review
            if mac["Crossover"].iloc[-1] == 1:
                return {"Tendency": "Bullish"}
            else:
                return {"Tendency": "Bearish"}
        else:
            return False
        
        
    # Optimize
    def optimize(self, st_range: list, lt_range: list) -> pd.DataFrame:
        
        """
        This method optimizes the strategy parameters.
        
        Parameters
        ----------
        param : list : st_range : Lower limits of the short period.
        ----------
        param : list : lt_range : Upper limits of the long period.
        
        Output
        -------
        return: pd.DataFrame : DataFrame containing returns for each parameter combination.
        """
        
        # Optimize
        combinations = []
        for i in range(st_range[0], st_range[1] + 1):
            for l in range(lt_range[0], lt_range[1] + 1):
                combinations.append([i, l])
        #Saving the initial params
        st_window = self.st_window
        lt_window = self.lt_window
        
        #Testing each combination
        returns = []
        for st_w, lt_w in combinations:
            #Modify each value into the strategy
            self.st_window = st_w
            self.lt_window = lt_w
            #Calculates the strategy with updated values
            self.calculate()
            #Backtest
            backtest = self.backtest()
            #Adding the paramethers and returns
            returns.append([st_w, lt_w, backtest.iloc[-1]])
        # Convert into a DataFrame
        returns = pd.DataFrame(returns, columns=["Short Term Window", "Long Term Window", "Final Return"])
        #Sorting Major to Minor
        returns = returns.sort_values(by="Final Return", ascending=False)
        
        #Backing to the initial paramethers
        self.st_window = st_window
        self.lt_window = lt_window
        self.calculate()
        
        return returns
    
    
    # Plot
    def plot(self, path: str = "Strategy1_MovingAverageCrossovers.png"):
        
        """
        This method plots our data and strategy.
        
        Parameters
        ----------
        param : str : path : Path where the plot will be saved (defaults to "Strategy1_MovingAverageCrossovers.png").
        
        Output
        -------
        return: NoneType : None
        """
        
        # Calculate
        mpf.plot(self.df, type="candle", style="yahoo",
                 title=dict(title="Strategy1 Moving Average Crossovers", fontsize=20,
                            y=0, x=0.55),
                 mav=(self.st_window, self.lt_window),
                 ylabel="Price", ylabel_lower="Volume", volume=True,
                 warn_too_much_data=self.df.shape[0], savefig=path,
                 figsize=(22,12), tight_layout=True)
        
        return


if __name__ == "__main__":
    
    # Getting data
    start_date = "2021-01-01"
    end_date = "2024-01-01"
    df = yf.download("MSFT", start=start_date, end=end_date, interval="1d")
    
    #Fixing yfinance MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    #Instantiate strategy
    St1 = Strategy1(df=df, st_window=9, lt_window=21, column="Close")
    #Calculates Strategy
    calculus = St1.calculate()
    print(calculus)
    print(f"Strategy 1, Calculus: {St1.strategy_calculus}")
    
    # Example who makes a signal
    print(Strategy1(df=df[:-1], st_window=9, lt_window=21, column="Close").calculate())
    
    #Backtest
    backtest = St1.backtest()
    print(f"Final Return with current paramethers: {backtest.iloc[-1]}")
    
    # Optimize
    st_range = [5,25]
    lt_range = [26,200]
    start = time.time()
    returns = St1.optimize(st_range, lt_range)
    print(f"Returns: {returns}")
    print(f"It takes {format(time.time()-start)} seconds")
    
    #fitting best params
    St1 = Strategy1(df=df, st_window=int(returns.iloc[0,0]), lt_window=int(returns.iloc[0,1]))
    St1.calculate()
    #Backtest
    backtest = St1.backtest()
    print(f"Final Retunrs with optimizated params: {backtest.iloc[-1]}")
    # Saving plot
    St1.plot()
    print("Before plotting")