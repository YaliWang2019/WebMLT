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
import itertools
from sklearn.model_selection import train_test_split
from matplotlib.pyplot import figure
from sklearn.linear_model import SGDRegressor
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from urllib.request import Request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from uuid import uuid4

csv_file = {}
X_database = {}
Y_database = {}
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

def scaling(id, scaleMode):
  df = csv_file[id]
  df_new = df.dropna()
  X = df_new.atemp.to_numpy()
  Y = df_new.cnt.to_numpy()
  if scaleMode == "standardization":
    # standardization
    Y = (Y - np.mean(Y)) / np.std(Y)
  elif scaleMode == "normalization":
    # normalization
    Y = (Y - np.min(Y)) / (np.max(Y) - np.min(Y))
  # error catching logic required here
  return (X, Y)

# Phase 3: data visualization (whole data visualization, training data visualization, and testing data visualization, return charts)

def scatterImg(id, scaleMode):
  (X, Y) = scaling(id, scaleMode)
  plt.clf()
  figure(figsize=(8, 6), dpi=80)
  plt.scatter(X, Y)
  
  plt.title("Visualize the full Dataset")
  plt.xlabel('X')
  plt.ylabel('Y')

  return (json.dumps({'imgScatter':img_to_base64(plt)}), 200)


  # Split the Dataset into Training and Test Set
def spliting(id, test_size=0.2, random_state=0, scaleMode="normalization"):
  (X, Y) = scaling(id, scaleMode)
  X_train_split, X_test_split, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=random_state)
  return (X_train_split, X_test_split, Y_train, Y_test)

def train_test_imgs(id, test_size, random_state):
  (X_train_split, X_test_split, Y_train, Y_test) = spliting(id, float(test_size), int(random_state))
  plt.clf()
  figure(figsize=(15, 6), dpi=80)
  plt.subplot(1, 2, 1) # row 1, col 2 index 1
  plt.scatter(X_train_split, Y_train)
  # trainImg = img_to_base64(plt)
  plt.title("Training Data")
  plt.xlabel('X_train')
  plt.ylabel('Y_train')

  plt.subplot(1, 2, 2) # index 2
  plt.scatter(X_test_split, Y_test)
  plt.title("Testing Data")
  plt.xlabel('X_test')
  plt.ylabel('Y_test')
  plt.tight_layout()
  trainTestestImg = img_to_base64(plt)

  return (json.dumps({'trainTestestImg': trainTestestImg}), 200)

# Phase 4: model training
# proving X_train, X_test, regressor, and Y_pred
def pre_train(id, test_size, random_state):
  (X_train_split, X_test_split, Y_train, Y_test) = spliting(id, test_size, random_state)
  # Create a 2D array for training and test data to make it compatible with
  # scikit-learn (This is specific to scikit-learn because of the way it accepts input data)
  X_train = X_train_split.reshape(-1, 1)
  X_test = X_test_split.reshape(-1, 1)

  # Initialize Model

  regressor = SGDRegressor()

  # Run Model Training
  regressor.fit(X_train, Y_train)

  # Predict on the Test Data
  Y_pred = regressor.predict(X_test)

  return (X_train, X_test, X_train_split, X_test_split, regressor, Y_train, Y_test, Y_pred)

  # plt.tight_layout()
def modelTraining(id, test_size, random_state):
  (_, _, _, X_test_split, _, _, Y_test, Y_pred) = pre_train(id, test_size, random_state)

  # Plot the predictions and the original test data
  plt.clf()
  figure(figsize=(8, 6), dpi=80)
  plt.plot(X_test_split, Y_test, 'go', label='True data', alpha=0.5)
  plt.plot(X_test_split, Y_pred, '--', label='Predictions', alpha=0.5)
  
  plt.title("Prediction")
  
  plt.legend(loc='best')

  return (json.dumps({'imgPrediction':img_to_base64(plt)}), 200)

# Phase 5: accuracy
def accuracy(id, test_size, random_state):
  (_, _, _, _, _, _, Y_test, Y_pred) = pre_train(id, test_size, random_state)
  meanAbErr = str(metrics.mean_absolute_error(Y_test, Y_pred))
  meanSqErr = str(metrics.mean_squared_error(Y_test, Y_pred))
  rootMeanSqErr = str(np.sqrt(metrics.mean_squared_error(Y_test, Y_pred)))
  # Evaluate the quality of the training (Generate Evaluation Metrics)
  return (json.dumps({'Mean Absolute Error:': meanAbErr, 'Mean Squared Error:': meanSqErr, 'Root Mean Squared Error:': rootMeanSqErr}), 200)

def confusionMatrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
  if normalize:
      cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

  plt.imshow(cm, interpolation='nearest', cmap=cmap)
  plt.title(title)
  plt.colorbar()
  tick_marks = np.arange(len(classes))
  plt.xticks(tick_marks, classes, rotation=45)
  plt.yticks(tick_marks, classes)

  fmt = '.2f' if normalize else 'd'
  thresh = cm.max() / 2.
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    plt.text(j, i, format(cm[i, j], fmt), horizontalalignment="center", color="white" if cm[i, j] > thresh else "black")

  plt.tight_layout()
  plt.ylabel('True label')
  plt.xlabel('Predicted label')
  return (img_to_base64(plt))

def makeConfusionMatrix(id, test_size, random_state):
  (_, _, _, _, _, _, Y_test, Y_pred) = pre_train(id, float(test_size), int(random_state))
  cm = confusion_matrix(Y_test, Y_pred)
  labels = ["+", "-"]
  matrix = confusionMatrix(cm, labels)  
  return (json.dumps({'confsMatrix': matrix}), 200)

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

