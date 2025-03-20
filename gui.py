from PySide6.QtWidgets import QApplication, QWidget


class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Калькулятор")
        self.setGeometry(200, 200, 350, 250)



if __name__ == "__main__":

    app = QApplication([])
    window = CalculatorApp()
    window.show()
    app.exec()
