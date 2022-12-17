from ctypes import Array
import sys
import subprocess
import json
import numpy as np
import pandas as pd
from linear_regression_chart import lr_fileUpload, lr_rmMissingvalues, lr_scatterImg, lr_train_test_imgs, lr_modelTraining, lr_accuracy
from logistic_regression import lgr_fileUpload, lgr_rmMissingvalues, lgr_scatterImg, lgr_train_test_imgs, lgr_modelTraining, lgr_accuracy, lgr_makeConfusionMatrix
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from urllib.request import Request
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.debug = True
CORS(app, resources={r"/*": {"origins": "*"}})

#---------------------------------------------------------------------#
# Linear Regression
@app.route('/datasets/linear_regression',methods=['POST'])
def lr_getUploadedFile():
    (data, res) = lr_fileUpload(request.files)
    return make_response(data, res)


@app.route('/datasets/<id>/linear_regression/missing_values',methods=['GET'])
def lr_removeMissingValues(id):
    rmResult = lr_rmMissingvalues(id)
    return make_response(rmResult)

@app.route('/datasets/<id>/linear_regression/scatter', methods = ['GET'])
def lr_make_scatter(id):
    scatterChart = lr_scatterImg(id, request.args.get('scaleMode'))
    return make_response(scatterChart)

@app.route('/datasets/<id>/linear_regression/train_test_datasets', methods = ['GET'])
def lr_traintest_imgs(id):
    charts = lr_train_test_imgs(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(charts)

@app.route('/datasets/<id>/linear_regression/model_training_result', methods = ['GET'])
def lr_prediction(id):
    pre_chart = lr_modelTraining(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(pre_chart)

@app.route('/datasets/<id>/linear_regression/calculation', methods = ['GET'])
def lr_calculations(id):
    results = lr_accuracy(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(results)

#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
# Logistic Regression
@app.route('/datasets/logistic_regression',methods=['POST'])
def lgr_getUploadedFile():
    (data, res) = lgr_fileUpload(request.files)
    return make_response(data, res)

@app.route('/datasets/<id>/logistic_regression/missing_values',methods=['GET'])
def lgr_removeMissingValues(id):
    rmResult = lgr_rmMissingvalues(id)
    return make_response(rmResult)

@app.route('/datasets/<id>/logistic_regression/scatter', methods = ['GET'])
def lgr_make_scatter(id):
    scatterChart = lgr_scatterImg(id, request.args.get('scaleMode'))
    return make_response(scatterChart)

@app.route('/datasets/<id>/logistic_regression/train_test_results', methods = ['GET'])
def lgr_traintest_imgs(id):
    charts = lgr_train_test_imgs(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(charts)

@app.route('/datasets/<id>/logistic_regression/model_training_result', methods = ['GET'])
def lgr_prediction(id):
    pre_chart = lgr_modelTraining(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(pre_chart)

@app.route('/datasets/<id>/logistic_regression/calculation', methods = ['GET'])
def lgr_calculations(id):
    results = lgr_accuracy(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(results)

@app.route('/datasets/<id>/logistic_regression/matrix', methods = ['GET'])
def lgr_getMatrix(id):
    confMatrixImg = lgr_makeConfusionMatrix(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(confMatrixImg)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5001)