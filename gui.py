import sys
import json
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QCheckBox
)

class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Калькулятор")
        self.setGeometry(200, 200, 350, 250)

        layout = QVBoxLayout()

        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText("Введите выражение (например, 2 + 2)")
        layout.addWidget(self.entry)

        self.float_checkbox = QCheckBox("Использовать float-режим", self)
        layout.addWidget(self.float_checkbox)

        self.calculate_button = QPushButton("Вычислить", self)
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)

        self.result_label = QLabel("Результат: ", self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def calculate(self):
        expression = self.entry.text()

        if not expression:
            QMessageBox.warning(self, "Ошибка", "Введите выражение!")
            return

        try:
            url = "http://localhost:8080"
            data = json.dumps({
                "expression": expression,
                "float_mode": self.float_checkbox.isChecked()  
            })
            headers = {"Content-type": "application/json"}
            response = requests.post(url, data=data, headers=headers)

            if response.status_code == 200:
                result = response.json().get("result")
                self.result_label.setText(f"Результат: {result}")
            else:
                error = response.json().get("error", "Неизвестная ошибка")
                QMessageBox.critical(self, "Ошибка", f"Ошибка сервера: {error}")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка соединения: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec())
