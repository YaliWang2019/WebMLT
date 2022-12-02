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


@app.route('/datasets/<id>/missingValues',methods=['GET'])
def removeMissingValues(id):
    rmResult = rmMissingvalues(id)
    return make_response(rmResult)

@app.route('/datasets/<id>/scatter', methods = ['GET'])
def make_scatter(id):
    scatterChart = scatterImg(id)
    return make_response(scatterChart)

@app.route('/datasets/<id>/train_test', methods = ['GET'])
def traintest_imgs(id):
    charts = train_test_imgs(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(charts)

@app.route('/datasets/<id>/model_training', methods = ['GET'])
def prediction(id):
    pre_chart = modelTraining(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(pre_chart)

@app.route('/datasets/<id>/calculation', methods = ['GET'])
def calculations(id):
    results = accuracy(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(results)

@app.route('/datasets/<id>/matrix', methods = ['GET'])
def getMatrix(id):
    confMatrixImg = makeConfusionMatrix(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(confMatrixImg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)