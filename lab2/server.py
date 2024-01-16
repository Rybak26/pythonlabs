from http.server import HTTPServer, CGIHTTPRequestHandler

def run_server():
    server_address = ("127.0.0.1",3333)
    print("Веб-сервер запущено!")
    httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
