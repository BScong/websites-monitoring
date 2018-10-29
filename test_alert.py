# To test the alerting logic, we create a server that we shut down and then restart

import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("<html><body><h1>TEST</h1></body></html>".encode())

def run(httpd):
    httpd.serve_forever()

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler)
    server = threading.Thread(target=run, args=[httpd])
    server.daemon = True
    server.start()
    print("Server running")
    time.sleep(60)
    httpd.shutdown()
    print("Server stopped")
    time.sleep(60)

    server = threading.Thread(target=run, args=[httpd])
    server.daemon = True
    server.start()
    time.sleep(600)
    httpd.shutdown()
    print("Server stopped")
