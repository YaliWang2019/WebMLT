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


def img_to_base64(plt):
  chart = BytesIO()
  plt.savefig(chart, format = 'png')
  chart.seek(0)
  output_chart = base64.b64encode(chart.getvalue())
  return str(output_chart, 'utf-8')