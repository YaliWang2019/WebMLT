import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np
from flask import Flask, render_template, request, make_response, jsonify
from io import BytesIO
import base64
from sklearn.model_selection import train_test_split
from matplotlib.pyplot import figure
from sklearn.linear_model import SGDRegressor
from sklearn import metrics
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from urllib.request import Request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from uuid import uuid4

csv_file = {}
# Phase (1). data collection (file upload):
def fileUpload(files):
  #  if request.method == 'POST':
  if files['file'].content_type != 'text/csv':
    return (json.dumps({'message': 'File must be a CSV'}), 400)
  
  df = pd.read_csv(files.get('file'))

  uuid = str(uuid4())

  csv_file[uuid] = df
  #print(df)
  return (json.dumps({'id': uuid}), 200)

# Phase (2). data preprocessing (removing missing values and scaling, return processed dataframe preview): 
def rmMissingvalues(id):
  df = csv_file[id]
  df_new = df.dropna()
  df_preview = df_new[0:5]
  return ((df_preview.to_json()), 200)


def scaling(df):
  origin_charts = []
  X = df.atemp.to_numpy()
  Y = df.cnt.to_numpy()

  # Scale the Data
  # Visualize the full Dataset
  # img_scatter
  Y = (Y - np.mean(Y)) / np.std(Y)

  plt.scatter(X, Y)
  origin_charts.append(img_to_base64(plt))
  plt.title("Visualize the full Dataset")
  plt.xlabel('X')
  plt.ylabel('Y')



  # Split the Dataset into Training and Test Set
  X_train_split, X_test_split, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
  plt.subplot(1, 2, 1) # row 1, col 2 index 1
  plt.scatter(X_train_split, Y_train)
  origin_charts.append(img_to_base64(plt))
  plt.title("Training Data")
  plt.xlabel('X_train')
  plt.ylabel('Y_train')

  plt.subplot(1, 2, 2) # index 2
  plt.scatter(X_test_split, Y_test)
  origin_charts.append(img_to_base64(plt))
  plt.title("Test Data")
  plt.xlabel('X_test')
  plt.ylabel('Y_test')

  # plt.tight_layout()

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
  plt.plot(X_test_split, Y_test, 'go', label='True data', alpha=0.5)
  plt.plot(X_test_split, Y_pred, '--', label='Predictions', alpha=0.5)
  origin_charts.append(img_to_base64(plt))
  plt.title("Prediction")
  
  plt.legend(loc='best')

  # Evaluate the quality of the training (Generate Evaluation Metrics)
  # print('Mean Absolute Error:', metrics.mean_absolute_error(Y_test, Y_pred))
  # print('Mean Squared Error:', metrics.mean_squared_error(Y_test, Y_pred))
  # print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(Y_test, Y_pred)))

  return origin_charts


def generate_dataset():
  X = np.linspace(0, 2, 100)
  Y = 1.5 * X + np.random.randn(*X.shape) * 0.2 + 0.5
  return X, Y



def img_to_base64(plt):
  chart = BytesIO()
  plt.savefig(chart, format = 'png')
  chart.seek(0)
  output_chart = base64.b64encode(chart.getvalue())
  return str(output_chart, 'utf-8')

