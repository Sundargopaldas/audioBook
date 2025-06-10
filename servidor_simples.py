import http.server
import socketserver
import os

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

# O servidor deve ser executado do diretório raiz do projeto (Nova pasta)

print(f"Servidor rodando em http://localhost:{PORT}")
print(f"Servindo arquivos de: {os.getcwd()}")
print("\nPara testar a narração, abra: http://localhost:8080/testar_narracao.html")

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    httpd.serve_forever() 