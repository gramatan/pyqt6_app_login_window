import sys
import time
from PyQt6 import QtCore, QtGui, QtWidgets


class LoginWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup UI
        self.setWindowTitle("Login App")
        self.layout = QtWidgets.QVBoxLayout(self)

        # PIN code indicator
        self.indicatorLayout = QtWidgets.QHBoxLayout()
        self.indicators = [QtWidgets.QLabel("○") for _ in range(4)]
        for indicator in self.indicators:
            self.indicatorLayout.addWidget(indicator)
        self.layout.addLayout(self.indicatorLayout)
        self.layout.setAlignment(self.indicatorLayout, QtCore.Qt.AlignmentFlag.AlignCenter)

        # Error message
        self.errorLabel = QtWidgets.QLabel()
        self.errorLabel.hide()
        self.layout.addWidget(self.errorLabel)

        # Custom keyboard
        self.keypadLayout = QtWidgets.QGridLayout()
        self.keys = [QtWidgets.QPushButton(str(i)) for i in range(0, 10)]
        self.backspaceButton = QtWidgets.QPushButton("⬅")
        for i, key in enumerate(self.keys):
            key.clicked.connect(self.add_character)
            self.keypadLayout.addWidget(key, i//3, i%3)
        self.backspaceButton.clicked.connect(self.remove_character)
        self.keypadLayout.addWidget(self.backspaceButton, 3, 2)
        self.layout.addLayout(self.keypadLayout)

        self.pin_code = ""

    def add_character(self):
        if len(self.pin_code) < 4:
            self.pin_code += self.sender().text()
            self.indicators[len(self.pin_code) - 1].setText("●")
            if len(self.pin_code) == 4:
                self.check_pin_code()

    def remove_character(self):
        if len(self.pin_code) > 0:
            self.pin_code = self.pin_code[:-1]
            self.indicators[len(self.pin_code)].setText("○")
            self.errorLabel.hide()

    def check_pin_code(self):
        for key in self.keys:
            key.setEnabled(False)
        self.backspaceButton.setEnabled(False)

        if self.pin_code == "1234":
            for indicator in self.indicators:
                indicator.setStyleSheet("color: green")
            QtCore.QTimer.singleShot(1000, self.show_success)
        else:
            for indicator in self.indicators:
                indicator.setStyleSheet("color: red")
            self.errorLabel.setText("Invalid PIN. Please try again.")
            self.errorLabel.show()
            for key in self.keys:
                key.setEnabled(True)
            self.backspaceButton.setEnabled(True)

    def show_success(self):
        self.close()
        self.successWindow = QtWidgets.QWidget()
        self.successWindow.setWindowTitle("Welcome")
        self.successLabel = QtWidgets.QLabel("PIN is correct")
        self.successLayout = QtWidgets.QVBoxLayout(self.successWindow)
        self.successLayout.addWidget(self.successLabel)
        self.successWindow.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
