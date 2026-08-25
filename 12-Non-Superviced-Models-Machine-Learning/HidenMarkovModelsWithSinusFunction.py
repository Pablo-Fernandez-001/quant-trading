# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 17:51:57 2026

@author: pabda
"""

#import libs
import numpy as np
from hmmlearn import hmm # pip install hmmlearn==0.3.2
import matplotlib.pyplot as plt


#generates the data from the Sinus Function
t = np.linspace(start=0, stop=8*np.pi, num=1500) # Tiempo
signal = np.sin(t)

# Visualize the generated signal
plt.figure(figsize=(22,12))
plt.plot(t, signal, label="Sinus function")
plt.title("Watched signal: Sinus function")
plt.xlabel("Time")
plt.ylabel("Value")
plt.legend()
plt.grid()
plt.show()

# Preparing all data to training the model
obs = signal.reshape(-1,1)

#Defining the HMM with 2 hidden states
model = hmm.GaussianHMM(n_components=2, covariance_type="full", random_state=1)

#Fitting the model with the observated data
model.fit(obs)

#Prediction to the hidden states
hidden_states = model.predict(obs)

#Plotting 
plt.figure(figsize=(22,12))
plt.scatter(t[hidden_states==0], signal[hidden_states==0], label="Sinus Function with 0 State", color="blue")
plt.scatter(t[hidden_states==1], signal[hidden_states==1], label="Sinus Function with 1 State", color="red")
plt.title("Hidden States in the Watched Signal")
plt.xlabel("Time")
plt.ylabel("Value")
plt.legend()
plt.grid()
plt.show()

# Interpretation to the hidden states
for i in range(model.n_components):
    states_length = sum(hidden_states == i)
    div = states_length/hidden_states.shape[0]
    print(f"The current state it's: {i}, duration: {states_length}")
    print(f"The state {i} reprecents a percentaje of {div}\n")
    
# Reminder:
#   - Markov states represent discrete conditions that a system can occupy at a given moment.
#   - In a Markov model, only the current state matters for predicting the next step.