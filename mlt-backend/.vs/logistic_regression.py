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

  