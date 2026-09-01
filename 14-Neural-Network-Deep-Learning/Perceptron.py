# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 02:04:59 2026

@author: pabda
"""

#import libs
import pandas as pd
import numpy as np
import torch # conda install pytorch | pip install torch
import torch.nn as nn # that help us to creat the neural networks
import torch.optim as optim # that help us to optimize the training process
import matplotlib.pyplot as plt
import networkx as nx # pip install networkx, that help us to show in a graphical mode the Neural Network and understand it

# Training dataframe
df = pd.DataFrame(data=[[5, 6, 2, 4, 1.5, 5.5, 6, 9, 12, 0, 14, 8, 3, 8.5, 2.5, 10, 0.5, 13],
                        [6, 7, 8, 4, 6, 7, 9, 8, 7, 5, 6, 7, 10, 6, 7, 8, 6, 5],
                        [1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1]]).T #That T means Transposed
df.columns =["Studied Hours","Sleep Hours", "Aprobed Class Yes/No (1/0)"]
print(df)


#Preparing data, we must to use tensors to our data
X = torch.tensor(df[["Studied Hours","Sleep Hours"]].values, dtype=torch.float32)
y = torch.tensor(df["Aprobed Class Yes/No (1/0)"].values, dtype=torch.float32).view(-1,1)

# Seed
torch.manual_seed(1)
np.random.seed(1)

#perceptron (model to made) This method it's like a container ho makes each operation inside herself
#first apply the input of the neural network 
perceptron = nn.Sequential(
    nn.Linear(in_features=2, out_features=1),
    nn.Sigmoid() # Activation
    )

print(f"Perceptron: {perceptron}")