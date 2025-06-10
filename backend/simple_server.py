import http.server
import socketserver
import json

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/v1/audiobooks/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = json.dumps({'audiobooks': []})
            self.wfile.write(response.encode())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = json.dumps({'message': 'Hello World'})
            self.wfile.write(response.encode())

PORT = 8001
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Servidor rodando na porta {PORT}")
    httpd.serve_forever() 