from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
from pathlib import Path
import structlog

# Настройка structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.KeyValueRenderer(),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.WriteLoggerFactory(file=open("server.log", "a")),
    wrapper_class=structlog.BoundLogger,
    context_class=dict,
)

logger = structlog.get_logger()
calc_path = Path(__file__).parent / "src" / "calc.exe"

class CalculatorHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = "WAITING"

    def transition_to(self, new_state):
        logger.info("State transition", from_state=self.state, to_state=new_state)
        self.state = new_state

    def do_POST(self):
        try:
            if self.state == "WAITING":
                self.transition_to("PROCESSING")
                self.handle_processing()
            elif self.state == "PROCESSING":
                self.transition_to("SENDING_RESPONSE")
                self.handle_sending_response()
            elif self.state == "SENDING_RESPONSE":
                self.transition_to("WAITING")
            else:
                self.transition_to("ERROR")
                self.handle_error("Invalid state")
        except Exception as e:
            self.transition_to("ERROR")
            self.handle_error(str(e))

    def handle_processing(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            data = json.loads(body)
            expression = data.get("expression")
            use_float = data.get("float_mode", False)

            if not isinstance(expression, str):
                raise ValueError("Expression must be a string")

            logger.info("Evaluating expression", expression=expression, float_mode=use_float)
            result = subprocess.run(
                [calc_path, "--float"] if use_float else [calc_path],
                input=expression,
                capture_output=True,
                text=True,
                check=True
            )
            self.calculation_result = result.stdout.strip()
            logger.info("Result of calculation", result=self.calculation_result)
        except (json.JSONDecodeError, ValueError, subprocess.CalledProcessError) as e:
            self.transition_to("ERROR")
            self.handle_error(str(e))

    def handle_sending_response(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"result": self.calculation_result}).encode("utf-8"))

    def handle_error(self, error_message):
        logger.error("Error occurred", error=error_message)
        self.send_response(500)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error": error_message}).encode("utf-8"))

def run(server_class=HTTPServer, handler_class=CalculatorHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    logger.info("Starting HTTP server", host="localhost", port=port)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
