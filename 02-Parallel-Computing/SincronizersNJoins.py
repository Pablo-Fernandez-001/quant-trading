# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 16:52:04 2026

@author: pabda
"""


import multiprocessing
import numpy as np


#Define the function

def rangeOperations(lowerLimit: int, topLimit: int, dictionary, key, sincronizer) -> None:
    value = 0
    for i in range(lowerLimit, topLimit + 1):
        value += np.sqrt((i * 3) + ((i + 15) / 10))

    sincronizer.acquire()
    dictionary[key] = value
    sincronizer.release()

    print(f"The getted value inside the range was [{lowerLimit}, {topLimit}] = {value}")
    

# we need to execute all proces from terminal only
if __name__ == "__main__":
    
    lowerLimits = [1000,2000,3000,4000,5000,6000,7000,8000]
    topLimits =   [2000,3000,4000,5000,6000,7000,8000,9000]
    
    # Shared memory dictionary
    manager = multiprocessing.Manager()
    dict_results = manager.dict()
    
    #Sincronizer
    mutex = multiprocessing.Lock()
    
    # initializen all process
    process_list = []
    for i in range(len(lowerLimits)):
        p = multiprocessing.Process(target=rangeOperations, kwargs={"lowerLimit":lowerLimits[i],"topLimit":topLimits[i],"dictionary":dict_results,"key":f"Process_{i}","sincronizer":mutex})
        
        
        process_list.append(p)
        p.start()
        
    # Wait to end all excecuting process
    for p in process_list:
        p.join()
        
    
    # Show dictionary by console
    print("\n\nShared Memory Object\n\n")
    print(dict_results.items())
    
#Reminder:
# - Synchronizers help us avoid data corruption and are perfect tools for orderly execution of parallel tasks.
# - Shared memory objects are useful for sharing, adding, or modifying information.
# - Using JOIN allows us to wait for threads or processes to finish executing.