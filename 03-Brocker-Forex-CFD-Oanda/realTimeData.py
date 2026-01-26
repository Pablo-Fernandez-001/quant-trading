# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 18:50:26 2026

@author: pabda
"""

import tpqoa
import pandas as pd
import numpy as np
import threading
import time

#connection
config_file = "config.cfg"
oanda = tpqoa.tpqoa(config_file)

#params
ticker = "EUR_USD"
n_prices = 5

#streaming
# each time who's the price changes give to us the ask and bid, but if the prices doesn't changes in a while
# makes the error
try:
    # if we only uses oanda.stream_data(instrument=ticker,stop=n_prices) could be stop another processes
    # for that reason we going to use parallel computing. And we only can show it on console if we only 
    # uses that form of the stream_data.
    oanda.stream_data(instrument=ticker,stop=n_prices)
except Exception as error:
    print(f"Time limit exceded: {error}")


# Creating a Dataframe to store all prices
df_prices = pd.DataFrame(columns=["time","bid","ask"])

# Function
def on_success(ticker,time_, bid,ask):
    """
    funtion to call each time who we going to get each information tic
    Parameters
    ----------
    ticker : TYPE
        DESCRIPTION.
    time_bid : TYPE
        DESCRIPTION.
    ask : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    global df_prices
    # create a new register with each requested data
    new_register = pd.DataFrame(data=[[time_, bid, ask]], columns=["time", "bid", "ask"])
    # add the new register to the existing data
    df_prices = pd.concat([df_prices, new_register], ignore_index=True)
    # printing the before requested
    print(f"Time: {time_}, Bid: {bid}, Ask: {ask}")
    
# Streaming with on_success
try:
    oanda.stream_data(instrument=ticker,stop=n_prices, callback=on_success)
    print(df_prices)
except Exception as error:
    print(f"Time limit exceded: {error}")
    
    
# Manual changes
dta = pd.DataFrame(columns=["time","bid","ask"])
stop_streaming = False
def streaming_data(ticker, n) -> None:
    
    counter = 0
    while counter <= n:
        time_, bid, ask = oanda.get_prices(instrument=ticker)
        print(f"Time: {time_}, Bid: {bid}, Ask: {ask}")
        new_register = pd.DataFrame(data=[[time_, bid, ask]], columns=["time", "bid", "ask"])
        # Concatenate
        global data
        data = pd.concat([data, new_register], ignore_index=True)
        # Show the excecution
        global stop_streaming
        if stop_streaming:
            break
        else:
            time.sleep(1)
        # Increase accounter
        counter += 1
        
# Excecuting function
streaming_data(ticker=ticker, n=5)
print(data)


# Parallel Excecution
threading.Thread(target=streaming_data, args=(ticker, np.inf)).start()
time.sleep(15)
stop_streaming = True

# Reminder:
# - It is vital to properly process the information received in real time and create an appropriate structure
# that allows us to continue running our program.