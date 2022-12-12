from ctypes import Array
import sys
import subprocess
import json
import numpy as np
import pandas as pd
from linear_regression_chart import fileUpload, rmMissingvalues, scatterImg, train_test_imgs, modelTraining, accuracy
from logistic_regression import lgrFileUpload, lgrRmMissingvalues, lgrScatterImg, lgr_train_test_imgs, lgrModelTraining, lgr_accuracy, lgrMakeConfusionMatrix
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
@app.route('/lrDatasets',methods=['POST'])
def lrGetUploadedFile():
    (data, res) = fileUpload(request.files)
    return make_response(data, res)


@app.route('/lrDatasets/<id>/missingValues',methods=['GET'])
def lrRemoveMissingValues(id):
    rmResult = rmMissingvalues(id)
    return make_response(rmResult)

@app.route('/lrDatasets/<id>/scatter', methods = ['GET'])
def lr_make_scatter(id):
    scatterChart = scatterImg(id, request.args.get('scaleMode'))
    return make_response(scatterChart)

@app.route('/lrDatasets/<id>/train_test', methods = ['GET'])
def lr_traintest_imgs(id):
    charts = train_test_imgs(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(charts)

@app.route('/lrDatasets/<id>/model_training', methods = ['GET'])
def lr_prediction(id):
    pre_chart = modelTraining(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(pre_chart)

@app.route('/lrDatasets/<id>/calculation', methods = ['GET'])
def lr_calculations(id):
    results = accuracy(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(results)

#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
# Logistic Regression
@app.route('/lgrDatasets',methods=['POST'])
def lgrGetUploadedFile():
    (data, res) = lgrFileUpload(request.files)
    return make_response(data, res)

@app.route('/lgrDatasets/<id>/missingValues',methods=['GET'])
def lgrRemoveMissingValues(id):
    rmResult = lgrRmMissingvalues(id)
    return make_response(rmResult)

@app.route('/lgrDatasets/<id>/scatter', methods = ['GET'])
def lgr_make_scatter(id):
    scatterChart = lgrScatterImg(id, request.args.get('scaleMode'))
    return make_response(scatterChart)

@app.route('/lgrDatasets/<id>/train_test', methods = ['GET'])
def lgr_traintest_imgs(id):
    charts = lgr_train_test_imgs(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(charts)

@app.route('/lgrDatasets/<id>/model_training', methods = ['GET'])
def lgr_prediction(id):
    pre_chart = lgrModelTraining(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(pre_chart)

@app.route('/lgrDatasets/<id>/calculation', methods = ['GET'])
def calculations(id):
    results = lgr_accuracy(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(results)

@app.route('/lgrDatasets/<id>/matrix', methods = ['GET'])
def lgrGetMatrix(id):
    confMatrixImg = lgrMakeConfusionMatrix(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(confMatrixImg)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5001)