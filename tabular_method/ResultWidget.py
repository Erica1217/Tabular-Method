import sys

from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from qtpy import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *


class ResultWidget(QWidget):

    def __init__(self, data):
        super(ResultWidget, self).__init__()
        self.data = data

        self.init_ui()

    def init_ui(self):
        self.resize(1000, 400)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ResultWidget()
    ex.show()
    sys.exit(app.exec_())