from ctypes import Array
import sys
import subprocess
import json
import numpy as np
import pandas as pd
from linear_regression_chart import lr_fileUpload, lr_rmMissingvalues, lr_scatterImg, lr_train_test_imgs, lr_modelTraining, lr_accuracy
from logistic_regression import lgr_fileUpload, lgr_rmMissingvalues, lgr_explore, lgr_getShape, lgr_makeConfusionMatrix, lgr_accuracy
from polynomial_regression import poly_fileUpload, poly_rmMissingvalues, poly_scatterImg, poly_train_test_imgs, poly_modelTraining, poly_accuracy
from k_means_clustering import km_fileUpload, km_rmMissingvalues, km_scatterImg, km_plot_cluster, km_estimate
from svm import svm_fileUpload, svm_rmMissingvalues, svm_scatter_plot, svm_train_test_plot, svm_solution, svm_confusion_matrix, svm_evaluation

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
def lr_trainTest_imgs(id):
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

@app.route('/datasets/<id>/logistic_regression/get_features', methods = ['GET'])
def lgr_show_features(id):
    featuresResponse = lgr_explore(id, request.args.get('scaleMode'))
    return make_response(featuresResponse)

@app.route('/datasets/<id>/logistic_regression/datasets_shapes', methods = ['GET'])
def lgr_getShapes(id):
    shapes = lgr_getShape(id, request.args.get('test_size'), request.args.get('random_state'), request.args.get('scaleMode'))
    return make_response(shapes)

@app.route('/datasets/<id>/logistic_regression/model_training_result', methods = ['GET'])
def lgr_getMatrix(id):
    confMatrixImg = lgr_makeConfusionMatrix(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(confMatrixImg)

@app.route('/datasets/<id>/logistic_regression/calculation', methods = ['GET'])
def lgr_calculations(id):
    results = lgr_accuracy(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(results)
#---------------------------------------------------------------------#
#---------------------------------------------------------------------#
# Polynomial Regression
@app.route('/datasets/polynomial_regression',methods=['POST'])
def poly_getUploadedFile():
    (data, res) = poly_fileUpload(request.files)
    return make_response(data, res)


@app.route('/datasets/<id>/polynomial_regression/missing_values',methods=['GET'])
def poly_removeMissingValues(id):
    rmResult = poly_rmMissingvalues(id)
    return make_response(rmResult)

@app.route('/datasets/<id>/polynomial_regression/scatter', methods = ['GET'])
def poly_make_scatter(id):
    scatterChart = poly_scatterImg(id, request.args.get('scaleMode'))
    return make_response(scatterChart)

@app.route('/datasets/<id>/polynomial_regression/train_test_results', methods = ['GET'])
def poly_traintest_imgs(id):
    charts = poly_train_test_imgs(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(charts)

@app.route('/datasets/<id>/polynomial_regression/model_training_result', methods = ['GET'])
def poly_prediction(id):
    pre_chart = poly_modelTraining(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(pre_chart)

@app.route('/datasets/<id>/polynomial_regression/calculation', methods = ['GET'])
def poly_calculations(id):
    results = poly_accuracy(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(results)
#---------------------------------------------------------------------#
#---------------------------------------------------------------------#
# K-Means Clustering
@app.route('/datasets/k_means_clustering',methods=['POST'])
def km_getUploadedFile():
    (data, res) = km_fileUpload(request.files)
    return make_response(data, res)

@app.route('/datasets/<id>/k_means_clustering/missing_values',methods=['GET'])
def km_removeMissingValues(id):
    rmResult = km_rmMissingvalues(id)
    return make_response(rmResult)

@app.route('/datasets/<id>/k_means_clustering/scatter', methods = ['GET'])
def km_make_scatter(id):
    scatterChart = km_scatterImg(id, request.args.get('scaleMode'))
    return make_response(scatterChart)

@app.route('/datasets/<id>/k_means_clustering/train_test_results', methods = ['GET'])
def km_traintest_imgs(id):
    charts = km_plot_cluster(id, request.args.get('random_state'), request.args.get('scaleMode'))
    return make_response(charts)

@app.route('/datasets/<id>/k_means_clustering/model_training_result', methods = ['GET'])
def km_prediction(id):
    pre_chart = km_estimate(id, request.args.get('random_state'), request.args.get('scaleMode'))
    return make_response(pre_chart)

# @app.route('/datasets/<id>/k_means_clustering/calculation', methods = ['GET'])
#def km_calculations(id):
#    results = km_accuracy(id, request.args.get('test_size'), request.args.get('random_state'))
#    return make_response(results)

#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
# SVM Model
@app.route('/datasets/svm',methods=['POST'])
def svm_getUploadedFile():
    (data, res) = svm_fileUpload(request.files)
    return make_response(data, res)

@app.route('/datasets/<id>/svm/missing_values',methods=['GET'])
def svm_removeMissingValues(id):
    rmResult = svm_rmMissingvalues(id)
    return make_response(rmResult)

@app.route('/datasets/<id>/svm/scatter', methods = ['GET'])
def svm_scatterPlot(id):
    scatterPlot = svm_scatter_plot(id, request.args.get('scaleMode'))
    return make_response(scatterPlot)

@app.route('/datasets/<id>/svm/train_test_results', methods = ['GET'])
def svm_trainTest(id):
    trainTestPlots = svm_train_test_plot(id, request.args.get('test_size'), request.args.get('scaleMode'))
    return make_response(trainTestPlots)

@app.route('/datasets/<id>/svm/show_solution', methods = ['GET'])
def svm_showSolution(id):
    solutionPlot = svm_solution(id, request.args.get('test_size'), request.args.get('scaleMode'))
    return make_response(solutionPlot)

@app.route('/datasets/<id>/svm/show_confusion_matrix', methods = ['GET'])
def svm_showConfMatrix(id):
    confMatrixImg = svm_confusion_matrix(id, request.args.get('test_size'), request.args.get('scaleMode'))
    return make_response(confMatrixImg)

@app.route('/datasets/<id>/svm/calculation', methods = ['GET'])
def svm_calculations(id):
    results = svm_evaluation(id, request.args.get('test_size'), request.args.get('random_state'))
    return make_response(results)
#---------------------------------------------------------------------#


if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5001)