from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
HOST = "0.0.0.0"
PORT = 8888
class NeuralHTTP(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write("{\"message\": \"Hello World!\"}".encode())
  def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

if __name__ == "__main__":
  httpd = HTTPServer((HOST, PORT), NeuralHTTP)
  print("Server started at http://%s:%s" % (HOST, PORT))
  httpd.serve_forever()