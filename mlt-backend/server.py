from ctypes import Array
import sys
import subprocess
import json
import numpy as np
import pandas as pd
from linear_regression_chart import fileUpload, rmMissingvalues, scatterImg, train_test_imgs, modelTraining, accuracy, makeConfusionMatrix
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from urllib.request import Request
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.debug = True
CORS(app, resources={r"/*": {"origins": "*"}})
@app.route('/files',methods=['POST'])
def getUploadedFile():
    (data, res) = fileUpload(request.files)
    return make_response(data, res)


@app.route('/missingValues',methods=['GET'])
def removeMissingValues():
    rmResult = rmMissingvalues(request.args.get('id'))
    return make_response(rmResult)

@app.route('/scatter', methods = ['GET'])
def make_scatter():
    scatterChart = scatterImg(request.args.get('id'))
    return make_response(scatterChart)

@app.route('/train_test', methods = ['GET'])
def traintest_imgs():
    charts = train_test_imgs(request.args.get('id'), request.args.get('test_size'), request.args.get('random_state'))
    return make_response(charts)

@app.route('/model_training', methods = ['GET'])
def prediction():
    pre_chart = modelTraining(request.args.get('id'), request.args.get('test_size'), request.args.get('random_state'))
    return make_response(pre_chart)

@app.route('/calculation', methods = ['GET'])
def calculations():
    results = accuracy(request.args.get('id'), request.args.get('test_size'), request.args.get('random_state'))
    return make_response(results)

@app.route('/matrix', methods = ['GET'])
def getMatrix():
    confMatrixImg = makeConfusionMatrix(request.args.get('id'), request.args.get('test_size'), request.args.get('random_state'))
    return make_response(confMatrixImg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)