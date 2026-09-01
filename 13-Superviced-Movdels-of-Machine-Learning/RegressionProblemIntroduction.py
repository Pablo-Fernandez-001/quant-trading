# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 18:41:58 2026

@author: pabda
"""

#import libs
import pandas as pd
from xgboost import XGBRegressor  # pip install xgboost
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

#read data
path = "../data/housing.csv"
df = pd.read_csv(path, sep=",")
columns = df.columns

#To know the variables distribution
fig, axes = plt.subplots(nrows=5, ncols=3, figsize=(22, 12))

for n, i in enumerate(axes.flatten()):
    
    if n < 14:
        df[columns[n]].plot(kind="hist", ax=i)
        i.set_title(columns[n])
    else:
        i.axis("off")
        i.text(0.5,0.5,"Each Columns Distribution Graphics", fontsize=14, ha="center", va="center", weight="bold")

plt.tight_layout()
plt.show()

#Split training and test data
x = df.drop("MEDV", axis=1) # All predictors variables without MENDV
y = df["MEDV"] # Target Variable (mean housing value)

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.20, random_state=1)

#Creating the model and training
model = XGBRegressor(max_depth=2, objective="reg:squarederror", random_state=1) # To don't learn specific values we uses the max depth in 2
# With 2 takes a bit better the patterns more than with a biggest number
model.fit(xtrain, ytrain)

#Predict training and test values
ytrainpred = model.predict(xtrain)

#ploting the prediction vs the real data
plt.figure(figsize=(22,12))
plt.scatter(ytrain,ytrainpred)
plt.ylabel("Real values: (ytrain)")
plt.xlabel("Real values: (ytrainpred)")
plt.title("Predictions vs Real values in train values")
plt.show()

ytestpred = model.predict(xtest)
plt.figure(figsize=(22,12))
plt.scatter(ytest,ytestpred)
plt.ylabel("Real values: (ytrain)")
plt.xlabel("Real values: (ytrainpred)")
plt.title("Predictions vs Real values in test values")
plt.show()

# Calculates and shows the mean squared error (MSE) with the training data
mse_training = mean_squared_error(y_true=ytrain, y_pred=ytrainpred)
print(f"Mean Squared Error into the training data: {mse_training}")

# Calculates and shows the mean squared error (MSE) with the test data
mse_test = mean_squared_error(y_true=ytest, y_pred=ytestpred)
print(f"Mean Squared Error into the test data: {mse_test}")

# Reminder:
#   - XGBoost is a powerful machine learning algorithm that uses decision trees and boosting
#     techniques to continuously improve model accuracy.