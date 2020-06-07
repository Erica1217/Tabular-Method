import sys

from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from qtpy import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from Monomial import Monomial

class PatrickWidget(QWidget):

    def __init__(self, data, uncoveredMinterm, NEPIList):
        super(PatrickWidget, self).__init__()
        self.data = data
        self.uncoveredMinterm = uncoveredMinterm
        self.NEPIList = NEPIList

        self.init_ui()

    def init_ui(self):
        self.resize(1000, 400)

    def petrick_method(self):
        polynomial = []
        # todo nepi List length가 1이면 바로 리턴가능
        # 첫 괄호와 두번째 괄호 곱셈
        p = []
        for i in range(len(self.NEPIList[0])):
            for j in range(len(self.NEPIList[1])):
                m = Monomial(self.NEPIList[0][i])
                m.add_pi(self.NEPIList[1][j])
                p.append()

        polynomial.append(p)

        for i in range(1,len(self.NEPIList)):
            p = []
            for j in range(len(self.NEPIList[0])):
                p += list(map(lambda x: x.add_pi(), polynomial[i-1]))

            polynomial.append(p)


        # for i in range(len(self.NEPIList)):
        #     for j in range(len(self.NEPIList[i])):


        return

    def next_btn_clicked(self):
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PatrickWidget()
    ex.show()
    sys.exit(app.exec_())