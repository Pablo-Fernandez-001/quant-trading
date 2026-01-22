# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 23:02:31 2026

@author: pabda
"""

import threading
import time

# Functions
def func1(secconds: float) -> None:
    """
    First functionts to make all in parallel

    Parameters
    ----------
    secconds : float
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    """
    
    while True:
        print("function 1 saying Hi!")
        time.sleep(secconds)
        
def func2(secconds: float) -> None:
    """
    Seccond functionts to make all in parallel

    Parameters
    ----------
    secconds : float
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    """
    
    while True:
        print("function 2 saying Hi!")
        time.sleep(secconds)

# Initializen threads
t0 = threading.Thread(target=func1, kwargs={"secconds":3}, name="Thread 1")
t1 = threading.Thread(target=func2, kwargs={"secconds":3}, name="Thread 2")
t0.start()
t1.start()

# informatives Variables
print(f"First thread name: {t0.name}")
print(f"Seccond thread name: {t1.name}")
print(f"Is this action comes from the first thread? {t0.is_alive()}")
print(f"Is this action comes from the seccond thread? {t1.is_alive()}")

# Remember
# -- Inside a process could execute and have one or many threads.
# -- Each thread inside a process shares common memory space, allowing to acces and modify the same data and variables
# -- For each thread could you assing an unic ID.