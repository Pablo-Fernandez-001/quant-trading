# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 14:53:22 2026

@author: pabda
"""

import multiprocessing
import numpy as np


#Define the function

def rangeOperations(lowerLimit: int, topLimit: int) -> None:
    """
    Makes a lot of operations to get one value

    Parameters
    ----------
    lowerLimit : int
        DESCRIPTION.
    topLimit : int
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    """
    
    value = 0
    for i in range(lowerLimit, topLimit +1):
        value += np.sqrt((i*3)+((i+15)/10))
        
    print(f"The getted value inside the rante was [{lowerLimit}, {topLimit}  {value}]")
    

# we need to execute all proces from terminal only
if __name__ == "__main__":
    
    lowerLimits = [1000,2000,3000,4000,5000,6000,7000,8000]
    topLimits =   [2000,3000,4000,5000,6000,7000,8000,9000]
    
    
    # initializen all process
    for i in range(len(lowerLimits)):
        p = multiprocessing.Process(target=rangeOperations, kwargs={"lowerLimit":lowerLimits[i],"topLimit":topLimits[i]})
        
        p.start()
        
        

# the process doesn't share the same memori size
# if a process it's a bit faster than other, could be end first no matters his order
# the process could share information but with a dictionary of common information, or shared memory
# threads and process could not return a value just if we uses an external thing to share like a dictionary or shared memory

# Reminder:
# - Processes are especially useful for activities that demand high computational efficiency.
# - Each process represents an independent instance of the Python interpreter, running in its own memory space.
# - In most cases, we should limit the number of running processes to the number of available cores on our computer.
# Otherwise, the operating system might start terminating running processes to maintain system operation.