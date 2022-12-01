from ctypes import Array
import sys
import subprocess
import json
import numpy as np
import pandas as pd
from linear_regression_chart import fileUpload, rmMissingvalues
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
    getFile = fileUpload(request.files.get('file'))
    return (json.dumps(json.loads(getFile), indent=4))

@app.route('/missingValues',methods=['GET'])
def removeMissingValues(df):
    rmResult = rmMissingvalues(df)
    return (json.dumps(json.loads(rmResult), indent=4))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)