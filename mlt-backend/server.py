import sys
import subprocess
import json
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from urllib.request import Request
from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
@app.route('/', methods = ['POST', 'OPTIONS', 'GET'])

def hello_world():
    if request.method == 'POST':
        name: str = request.json['name']
        return make_response(json.dumps({"messages": "Hello, " + name + "!"}).encode(), 200)
    if request.method == 'OPTIONS':
        return make_response("{}", 204)
    if request.method == 'GET':
        return make_response(json.dumps({"messages": "Hello, World!"}).encode(), 200)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)