import sys
import subprocess
from scipy import print_Hello
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from urllib.request import Request
from flask import Flask, render_template, request
#app = Flask(__name__)

#@app.route('/', methods=['GET', 'POST'])
#def form():
#    return render_template('index.html')

#@app.route('/hello', methods=['GET', 'POST'])
#def hello():
#    return render_template('index.html', say=request.form['name'])

HOST = "0.0.0.0"
PORT = 8888

items = {
    "name": ""
}

class NeuralHTTP(BaseHTTPRequestHandler):    

    def do_GET(self):
        name = ""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(("Hello," + name + "!").encode())

#        output = subprocess.check_output([sys.executable, "scipy.py", name])
#        return output
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

if __name__ == "__main__":
     httpd = HTTPServer((HOST, PORT), NeuralHTTP)
     print("Server started at http://%s:%s" % (HOST, PORT))
     httpd.serve_forever()