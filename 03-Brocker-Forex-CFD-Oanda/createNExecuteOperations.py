# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 15:42:24 2026

@author: pabda
"""

import tpqoa

# connection to api

oanda = tpqoa.tpqoa(conf_file="config.cfg")


# Create Buy Position EUR-USD
ticker = "EUR_USD"
prices = oanda.get_prices(instrument=ticker)
current_price = (prices[1] + prices[2]) / 2
# buy_order = oanda.create_order(instrument=ticker, units=1000, sl_distance=0.01, tp_price=round(current_price+0.01, 4), ret=True)
buy_order = oanda.create_order(instrument=ticker, units=1000, sl_distance=0.01, tp_price = round(round(current_price, 5) + 0.01, 5), ret=True)


#Show active positions
print(oanda.get_positions())


# Close position EUR_USD with a sell
ticker = "EUR_USD"
sell_order = oanda.create_order(instrument=ticker, units=-1000)

# Print account transactions 
oanda.print_transactions()

#Get account information
account_info = oanda.get_account_summary()
print(f"The account performance was: {account_info["pl"]}")


# Complete historical transaction
historical_transactions = oanda.get_transactions()

# Get specific transaction information
print(oanda.get_transaction(tid=buy_order["id"]))

# Reminder:
# - Order creation should be done with caution, as errors in order configuration or execution can
# result in financial losses.