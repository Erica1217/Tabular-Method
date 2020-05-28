import sys

from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from qtpy import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from EPIWidget import EPIWidget

class PIWidget(QWidget):

    def __init__(self, data):
        super(PIWidget, self).__init__()
        self.data = data
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
        self.piTable1.setRowCount(len(self.data))
        self.set_table1()
        self.piTable1.setHorizontalHeaderLabels(["# of 1s", "Minterm", "Binary","Combined"])
        self.piTable1.setColumnWidth(0, 50)
        self.piTable1.setColumnWidth(1, 50)
        self.piTable1.setColumnWidth(2, 50)


        nextBtn = QPushButton("next")
        nextBtn.clicked.connect(self.next_btn_clicked)

        vLayout.addWidget(titleLabel)
        vLayout.addWidget(self.piTable1)
        vLayout.addWidget(nextBtn)

        self.setLayout(vLayout)

    def set_table1(self):
        for i in range(len(self.data)):
            minterm , isDontcare, isCombined = self.data[i]
            print(minterm.getNum1(),'*')
            items = [ QTableWidgetItem(str(minterm.getNum1())),
                      QTableWidgetItem(str(minterm.numbers)),
                      QTableWidgetItem(minterm.binary),
                      QTableWidgetItem('v' if isCombined else '')]

            for j in range(4):
                items[j].setTextAlignment(Qt.AlignCenter)
                self.piTable1.setItem(i, j, items[j])

    def next_btn_clicked(self):
        self.thisWindow = EPIWidget()
        self.thisWindow.show()

    def find_pi(self):
        self.midterm.split(',')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PIWidget()
    ex.show()
    sys.exit(app.exec_())
