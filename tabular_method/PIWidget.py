import sys

from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from qtpy import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from EPIWidget import EPIWidget

class PIWidget(QWidget):

    def __init__(self, piTableValue=None):
        super(PIWidget, self).__init__()
        self.piTableValue = piTableValue
        self.init_ui()

    def init_ui(self):
        self.resize(800, 400)

        vLayout = QVBoxLayout()
        titleLabel = QLabel("PI TABLE")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setFont(QtGui.QFont("Arial Rounded MT Bold", 20))

        self.piTable1 = QTableWidget()
        # self.piTable2 = QTableWidget()

        self.piTable1.setColumnCount(4)
        self.piTable1.setRowCount(10)
        self.piTable1.setHorizontalHeaderLabels(["# of 1s", "Minterm", "Binary","Combined"])

        nextBtn = QPushButton("다음")
        nextBtn.clicked.connect(self.next_btn_clicked)

        vLayout.addWidget(titleLabel)
        vLayout.addWidget(self.piTable1)
        vLayout.addWidget(nextBtn)

        self.setLayout(vLayout)

    def next_btn_clicked(self):
        self.thisWindow = EPIWidget()
        self.thisWindow.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PIWidget()
    ex.show()
    sys.exit(app.exec_())