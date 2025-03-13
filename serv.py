from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
import subprocess
from pathlib import Path

calc_path = Path(__file__).parent / "src" / "calc.exe"

class CalculatorHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            use_float = query_params.get("float", ["0"])[0] == "1"
            
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length).decode("utf-8")
            
            try:
                expression = json.loads(body)
                if not isinstance(expression, str):
                    raise ValueError("Expression must be a string")
            except (json.JSONDecodeError, ValueError):
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON or expression format"}).encode("utf-8"))
                return
            
            try:
                result = subprocess.run(
                    [calc_path, "--float"] if use_float else [calc_path],
                    input=expression,
                    capture_output=True,
                    text=True,            
                    check=True  
                )

                output = result.stdout.strip()  
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"result": output}).encode("utf-8"))
            except subprocess.CalledProcessError as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": e.stderr}).encode("utf-8"))
        except Exception as e:
            self.send_response(501)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

def run(server_class=HTTPServer, handler_class=CalculatorHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    
    print(f"Starting HTTP server on http://localhost:{port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
