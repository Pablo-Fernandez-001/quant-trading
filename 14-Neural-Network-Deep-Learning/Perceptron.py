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
df.columns =["Studied Hours","Sleep Hours", "Approved Class Yes/No (1/0)"]
print(df)


studied = df["Studied Hours"]
sleeped = df["Sleep Hours"]
Approved = df["Approved Class Yes/No (1/0)"]

#Preparing data, we must to use tensors to our data
X = torch.tensor(df[["Studied Hours","Sleep Hours"]].values, dtype=torch.float32)
y = torch.tensor(df["Approved Class Yes/No (1/0)"].values, dtype=torch.float32).view(-1,1)

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

#Ploting perceptron structure
def plot_perceptron() -> None:
    """
    This function plots the perceptron sctucture
    """
    
    # Creating dirirected graph
    G = nx.DiGraph()
    G.add_nodes_from([1, 2], layer=0) # 1 output, 2 input, that's the 0 layer
    G.add_nodes_from([3], layer=1) # 3 output, that's the 1st layer
    G.add_edges_from([(1,3),(2,3)]) #Tupples connected input with output
    pos = nx.multipartite_layout(G, subset_key="layer")
    nx.draw(G, pos, with_labels=True, node_size=200, node_color="lightblue", font_size=10, font_weight="bold")
    plt.title("Perceptron Structure")
    plt.show()
    
#plotting perceptron structure
plot_perceptron()

# Define the loss and optimization function
loss_func = nn.BCELoss() # Binary Cross Entropy Loss (binary problems 1/0)
optimizer = optim.SGD(perceptron.parameters(), lr=0.1) #Stochastic Gradient Descent, a biggest learning rate makes 
# the model learn faster, and a lower than the oposite, to more complex problems, it's suggested to use 0.01 in learning rate (lr)

#Training
# List to save the loss values and accuracy values
loss_values = []
accuracy_values = []

#Model Training
num_epochs = 1_000

for epoch in range(num_epochs):
    #Forward Step
    outputs = perceptron(X) 
    loss = loss_func(outputs, y)
    
    #Backgward and optimization
    optimizer.zero_grad() # Stablish the gradinet in 0, to update the weights
    loss.backward()
    optimizer.step()
    
    # Calculates and store the loss of the model
    loss_values.append(loss.item())
    
    #Calculates the accuracy
    predicted = (outputs > 0.5).float()
    accuracy = (predicted==y).float().mean().item()
    accuracy_values.append(accuracy)
    
    #Print loss and accuracy each 100 iteration
    if (epoch + 1) % 100 == 0:
        print(f"Epoch [{epoch + 1} / {num_epochs}], Loss: {loss.item():.4f}, Accuracy: {accuracy:.4f}")

# Plotting the loss and accuracy
epochs = range(1, len(loss_values)+1)

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(18,6))

# Loss Graphic (Model's Optimization)
axes[0, 0].plot(epochs, loss_values, "b--", label="Loss")
axes[0, 0].set_xlabel("Iterations")
axes[0, 0].set_ylabel("Loss")
axes[0, 0].set_title("Loss across the training", size=20)
axes[0, 0].legend()

# Accuracy Graphic (Model's Optimization)
axes[0, 1].plot(epochs, accuracy_values, "g--", label="Accuracy")
axes[0, 1].set_xlabel("Iterations")
axes[0, 1].set_ylabel("Accuracy")
axes[0, 1].set_title("Accuracy across the training", size=20)
axes[0, 1].legend()

# Original Dataset
axes[1, 0].scatter(studied[Approved == 1],sleeped[Approved==1],color="green", label="Approved")
axes[1, 0].scatter(studied[Approved == 0],sleeped[Approved==0],color="red", label="Rejected")
axes[1, 0].set_xlabel("Studied Hours")
axes[1, 0].set_ylabel("Sleeped Hours")
axes[1, 0].set_title("Original Dataset", size=20)
axes[1, 0].legend()


#Predicted Dataset
pred = np.round(perceptron(X).detach().numpy()).flatten()
axes[1, 1].scatter(studied[pred == 1],sleeped[pred==1],color="green", label="Approved Prediction")
axes[1, 1].scatter(studied[pred == 0],sleeped[pred==0],color="red", label="Rejected Prediction")
axes[1, 1].set_xlabel("Studied Hours")
axes[1, 1].set_ylabel("Sleeped Hours")
axes[1, 1].set_title("Prediction Dataset", size=20)
axes[1, 1].legend()

# Extract Model Weights
weights = perceptron[0].weight.detach().numpy()
b = perceptron[0].bias.detach().numpy() # Bias

#Calculates the Line Desition Coeficient Frontline 
w1, w2 = weights[0]
b = b[0]
slope = -w1 / w2
intercept = -b / w2

# Tracing Frontline Desition like a line
xvals = np.array([studied.min(), studied.max()])
yvals = slope * xvals + intercept
axes[1, 1].plot(xvals, yvals, "k--", lw=2, label="Desition Frontline")
axes[1, 1].legend()

plt.tight_layout()
plt.show()

# Reminder:
#   - Neural networks are computational models inspired by the human brain, used to solve complex
#     deep learning problems.
#   - The perceptron is the basic unit of a neural network, capable of performing simple classification
#     and supervised learning operations.