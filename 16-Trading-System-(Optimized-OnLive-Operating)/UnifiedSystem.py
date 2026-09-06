# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 01:12:42 2026

@author: pabda
"""

#import libs
import multiprocessing
import datetime
import pytz # pip install pytz
import time
# Own libraries
from IntradaySystem import Intraday_System
from SwingSystem import Swing_System
from PositionSystem import Position_System


#Excecuting
if __name__ == "__main__":
    #Making a parallel excecution each system
    process_intraday_system =  multiprocessing.Process(target=Intraday_System)
    process_swing_system =  multiprocessing.Process(target=Swing_System)
    process_position_system =  multiprocessing.Process(target=Position_System)
    #initialize
    process_intraday_system.start()
    process_swing_system.start()
    process_position_system.start()
    
    #Defining New York time zone
    ny_tz = pytz.timezone("America/New_York")
    #Getting current time
    current_time = datetime.datetime.now(ny_tz)
    #Defining New York Close (4:00 PM ET)
    market_close = current_time.replace(hour=16, minute=0, second=0, microsecond=0)
    
    # Sleeping our code until cease his excecution
    time.sleep((market_close - current_time).seconds)
    #Stopping Executing Processes
    process_intraday_system.kill()
    process_swing_system.kill()
    process_position_system.kill()
    print("The trading session has ended!")

# Reminder:
#   - Each Trading System is running in a separate process in parallel.
#   - It is recommended to run this script from the terminal to see the console output.
    