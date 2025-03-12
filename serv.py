from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", "text/plain") 
        self.end_headers()
        self.wfile.write(b"serv!") 

# Запуск сервера
def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=4443):
    server_address = ("", port)  
    httpd = server_class(server_address, handler_class)
    print(f"Начало работы сервера {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
