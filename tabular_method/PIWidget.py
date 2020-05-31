import sys

from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from qtpy import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from EPIWidget import EPIWidget
import copy

class PIWidget(QWidget):

    def __init__(self, data, mintermList, dontcareList):

        super(PIWidget, self).__init__()
        self.isFinish=False
        self.data = data
        self.mintermList = mintermList
        self.dontcareList = dontcareList
        self.init_ui()

    def init_ui(self):
        self.resize(800, 400)

        vLayout = QVBoxLayout()
        titleLabel = QLabel("PI TABLE")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setFont(QtGui.QFont("Arial Rounded MT Bold", 20))

        hLayout = QHBoxLayout()

        self.piTable1 = QTableWidget()
        self.piTable2 = QTableWidget()
        self.set_table(self.piTable1, self.data)

        hLayout.addWidget(self.piTable1)
        hLayout.addWidget(QLabel('->'))
        hLayout.addWidget(self.piTable2)

        self.nextBtn = QPushButton("next")
        self.nextBtn.clicked.connect(self.next_btn_clicked)

        vLayout.addWidget(titleLabel)
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.nextBtn)

        self.setLayout(vLayout)

    def set_table(self, table, data):
        table.setColumnCount(4)
        table.setRowCount(len(data))
        table.setHorizontalHeaderLabels(["# of 1s", "Minterm", "Binary","Combined"])
        table.setColumnWidth(0, 50)
        table.setColumnWidth(2, 50)

        for i in range(len(data)):
            minterm , isDontcare, isCombined = data[i]
            items = [ QTableWidgetItem(str(minterm.num1)),
                      QTableWidgetItem(str(minterm.numbers)),
                      QTableWidgetItem(minterm.binary),
                      QTableWidgetItem('v' if isCombined else '')]

            for j in range(4):
                items[j].setTextAlignment(Qt.AlignCenter)
                table.setItem(i, j, items[j])

    def next_btn_clicked(self):
        if self.isFinish:
            self.thisWindow = EPIWidget(self.data, self.mintermList, self.dontcareList)
            self.thisWindow.show()
        else:
            tmp = self.find_pi(self.data)
            self.set_table(self.piTable2, tmp)
            self.set_table(self.piTable1, self.data)
            if not self.isFinish:
                self.data = tmp

    def find_pi(self, data):
        self.isFinish=True
        result = []
        for i in range(len(data)-1):
            for j in range(i+1, len(data)):
                arr_tmp = data[i][0].numbers + data[j][0].numbers
                if self.__get_hd(data[i][0].binary, data[j][0].binary) <= 1 and \
                        len(arr_tmp) == len(set(arr_tmp)):
                    self.isFinish=False
                    t = copy.deepcopy(data[i])
                    t[0].combineNum(data[j][0].numbers)
                    self.data[i][2] = True
                    self.data[j][2] = True
                    t[2]=False
                    result.append(t)

        dedup_result=[]
        for i in range(len(result)-1):
            is_dedup=False
            for j in range(len(dedup_result)):
                if result[i][0].numbers == dedup_result[j].numbers:
                    is_dedup=True
                    break
            if not is_dedup:
                dedup_result.append(result[i][0])

        dedup_result = sorted(result, key=lambda x:x[0].num1)

        if self.isFinish:
            self.nextBtn.setText('find EPI')
            self.nextBtn.setStyleSheet("background-color: blue")

        return dedup_result

    def __get_hd(self, bin1, bin2):
        result=0
        for i in range(len(bin1)):
            if bin1[i] != bin2[i]:
                result += 1

        return result



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PIWidget()
    ex.show()

    sys.exit(app.exec_())
