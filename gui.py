from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox


class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Калькулятор")
        self.setGeometry(200, 200, 350, 250)
        
        # Вертикальный макет
        layout = QVBoxLayout()

        # Поле для ввода выражения
        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText("Введите выражение (например, 2 + 2)")
        layout.addWidget(self.entry)

        # Чекбокс для float-режима
        self.float_checkbox = QCheckBox("Использовать float-режим", self)
        layout.addWidget(self.float_checkbox)

        # Кнопка для вычисления
        self.calculate_button = QPushButton("Вычислить", self)
        layout.addWidget(self.calculate_button)

        # Поле для вывода результата
        self.result_label = QLabel("Результат: ", self)
        layout.addWidget(self.result_label)

        # Установка layout
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = CalculatorApp()
    window.show()
    app.exec()
