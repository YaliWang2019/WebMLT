import os
import requests
import zipfile
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np
from flask import Flask, render_template
from io import BytesIO
import base64
from sklearn.model_selection import train_test_split
from matplotlib.pyplot import figure
from sklearn.linear_model import SGDRegressor
from sklearn import metrics
app = Flask(__name__)
app.debug = True

@app.route('/index')
@app.route('/linearregression_chart',methods=['GET'])

def linearregression_chart(df):
  
  chartset = np.array([])
  origin_charts = []
  X = df.atemp.to_numpy()
  Y = df.cnt.to_numpy()

  # Scale the Data
  # Visualize the full Dataset
  # img_scatter
  Y = (Y - np.mean(Y)) / np.std(Y)
  img_scatter = plt.scatter(X, Y)
  
  # Split the Dataset into Training and Test Set
  X_train_split, X_test_split, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
  plt.subplot(1, 2, 1) # row 1, col 2 index 1
  img_train = plt.scatter(X_train_split, Y_train)
  plt.title("Training Data")
  plt.xlabel('X_train')
  plt.ylabel('Y_train')

  plt.subplot(1, 2, 2) # index 2
  img_test = plt.scatter(X_test_split, Y_test)
  plt.title("Test Data")
  plt.xlabel('X_test')
  plt.ylabel('Y_test')

  plt.tight_layout()

  # Create a 2D array for training and test data to make it compatible with
  # scikit-learn (This is specific to scikit-learn because of the way it accepts input data)
  X_train = X_train_split.reshape(-1, 1)
  X_test = X_test_split.reshape(-1, 1)
  X_train.shape, X_test.shape

  # Initialize Model

  regressor = SGDRegressor()

  # Run Model Training
  regressor.fit(X_train, Y_train)

  # Predict on the Test Data
  Y_pred = regressor.predict(X_test)

  # Plot the predictions and the original test data
  X_test_split.shape, Y_pred.shape, Y_test.shape

  plt.clf()
  img_prediction = plt.plot(X_test_split, Y_test, 'go', label='True data', alpha=0.5)
  img_prediction = plt.plot(X_test_split, Y_pred, '--', label='Predictions', alpha=0.5)
  plt.legend(loc='best')

  # Evaluate the quality of the training (Generate Evaluation Metrics)
  print('Mean Absolute Error:', metrics.mean_absolute_error(Y_test, Y_pred))
  print('Mean Squared Error:', metrics.mean_squared_error(Y_test, Y_pred))
  print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(Y_test, Y_pred)))

  origin_charts.append(img_scatter)
  
  img_scatter_out = BytesIO()
  plt.cla()
  plt.savefig(img_scatter_out, format = 'png')
  img_scatter_out.seek(0)
  chart_png = base64.b64encode(img_scatter_out.getvalue())
  chartset = np.append(img_scatter, chart_png)
  return str(chart_png, "utf-8")


def generate_dataset():
  X = np.linspace(0, 2, 100)
  Y = 1.5 * X + np.random.randn(*X.shape) * 0.2 + 0.5
  return X, Y





