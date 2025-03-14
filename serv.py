from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
import subprocess
from pathlib import Path
import structlog  # Импортируем structlog

# Настройка structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),  # Добавляем временную метку
        structlog.processors.add_log_level,  # Добавляем уровень логирования
        structlog.processors.KeyValueRenderer(),  # Простой текстовый вывод в консоль
        structlog.processors.JSONRenderer(),  # Экспорт в JSON
    ],
    logger_factory=structlog.WriteLoggerFactory(
        file=open("server.log", "a")  # Запись логов в файл
    ),
    wrapper_class=structlog.BoundLogger,
    context_class=dict,
)

# Создаём логгер
logger = structlog.get_logger()

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
            except (json.JSONDecodeError, ValueError) as e:
                logger.error("Invalid JSON or expression format", error=str(e))  # Логируем ошибку
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON or expression format"}).encode("utf-8"))
                return

            try:
                logger.info("Evaluating expression", expression=expression, float_mode=use_float)  # Логируем запрос
                result = subprocess.run(
                    [calc_path, "--float"] if use_float else [calc_path],
                    input=expression,
                    capture_output=True,
                    text=True,
                    check=True
                )

                output = result.stdout.strip()
                logger.info("Result of calculation", result=output)  # Логируем результат
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"result": output}).encode("utf-8"))
            except subprocess.CalledProcessError as e:
                logger.error("Calculator error", error=e.stderr)  # Логируем ошибку калькулятора
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": e.stderr}).encode("utf-8"))
        except Exception as e:
            logger.critical("Unexpected error", error=str(e))  # Логируем критические ошибки
            self.send_response(501)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

def run(server_class=HTTPServer, handler_class=CalculatorHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)

    logger.info("Starting HTTP server", host="localhost", port=port)  # Логируем запуск сервера
    httpd.serve_forever()

if __name__ == "__main__":
    run()