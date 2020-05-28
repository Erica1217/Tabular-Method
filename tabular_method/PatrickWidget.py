import sys

from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from qtpy import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *

class PatrickWidget(QWidget):

    def __init__(self, data):
        super(PatrickWidget, self).__init__()
        self.data = data
        self.init_ui()

    def init_ui(self):
        self.resize(1000, 400)

        vLayout = QVBoxLayout()
        titleLabel = QLabel("EPI TABLE")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setFont(QtGui.QFont("Arial Rounded MT Bold", 20))

        hLayout = QHBoxLayout()

        self.piTable1 = QTableWidget()
        self.piTable2 = QTableWidget()

        self.piTable1.setColumnCount(4)
        self.piTable1.setRowCount(10)
        self.piTable1.setHorizontalHeaderLabels(["PI","10","11"])

        self.piTable2.setColumnCount(4)
        self.piTable2.setRowCount(10)
        self.piTable2.setHorizontalHeaderLabels(["PI", "10", "11"])

        nextLabel = QLabel("->")

        hLayout.addWidget(self.piTable1)
        hLayout.addWidget(nextLabel)
        hLayout.addWidget(self.piTable2)

        nextBtn = QPushButton("다음")
        nextBtn.clicked.connect(self.next_btn_clicked)

        vLayout.addWidget(titleLabel)
        vLayout.addLayout(hLayout)
        vLayout.addWidget(nextBtn)

        self.setLayout(vLayout)

    def next_btn_clicked(self):
        # self.thisWindow = EPIWidget()
        self.thisWindow.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PatrickWidget()
    ex.show()
    sys.exit(app.exec_())