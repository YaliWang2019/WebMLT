import sys
import subprocess
import json
from chart import simple_chart
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from urllib.request import Request
from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
@app.route('/', methods = ['POST', 'OPTIONS', 'GET'])

def hello_world():
    #Use POST method to post the data body as json body
    #if request.method == 'POST':
    #    name: str = request.json['name']
    #    return make_response(json.dumps({"messages": "Hello Post, " + name + "!"}).encode(), 200)
    #Preflight request to exam if the current request
    if request.method == 'OPTIONS': 
        #204 status: success but no content
        return make_response("{}", 204) 
    if request.method == 'GET':
        return make_response(json.dumps({"messages": "Hello Get, World!"}).encode(), 200)
    if request.method == 'POST':
        name: str = request.json['x']
        return make_response(json.dumps(simple_chart(name)).encode(), 200)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)