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
        self.petrick_method()

    def init_ui(self):
        self.resize(1000, 400)
        vLayout = QVBoxLayout()
        titleLabel = QLabel("Petrick Method")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setFont(QtGui.QFont("Arial Rounded MT Bold", 20))

        hLayout = QHBoxLayout()

        self.nextBtn = QPushButton("next")
        self.nextBtn.clicked.connect(self.next_btn_clicked)

        vLayout.addWidget(titleLabel)
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.nextBtn)
        self.setLayout(vLayout)

    def petrick_method(self):
        polynomial = []
        # todo nepi List length가 1이면 바로 리턴가능
        # 첫 괄호와 두번째 괄호 곱셈

        # uncoveredMintermDick = dict()
        # print(self.NEPIList)
        # for i in range(len(self.NEPIList)):
        #     # print(self.NEPIList[i],"*")
        #     for j in range(len(self.NEPIList[i].numbers)):
        #         if self.NEPIList[i].numbers[j] not in uncoveredMintermDick:
        #             uncoveredMintermDick[self.NEPIList[i].numbers[j]] = []
        #
        #         uncoveredMintermDick[self.NEPIList[i].numbers[j]].append(self.NEPIList[i].getName())
        #
        # uncoveredMintermList =[]
        # # dict -> list
        # for key, value in uncoveredMintermDick.iteritems():
        #     temp = [key, value]
        #     uncoveredMintermList.append(temp)

        p = []
        for i in range(len(self.NEPIList[0])):
            for j in range(len(self.NEPIList[1])):
                m = set()
                m.add(self.NEPIList[0][i].getName())
                m.add(self.NEPIList[1][j].getName())
                p.append(m.copy())

        polynomial.append(p)

        for i in range(1,len(self.NEPIList)):
            p = []
            for j in range(len(self.NEPIList[i])):
                # print(polynomial[i-1])
                # 각 단항식에 추가

                # cur = []
                for k in range(len(polynomial[i-1])):
                    s = polynomial[i-1][k].copy()
                    s.add(self.NEPIList[i][j].getName())
                    p.append(s)
                # p += cur
            polynomial.append(p)

        print(polynomial[len(self.NEPIList)-1])
        # polynomial = polynomial[len(self.NEPIList)-1]

        for i in range(len(polynomial)):
            print(polynomial[i])

        return

    def next_btn_clicked(self):
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PatrickWidget()
    ex.show()
    sys.exit(app.exec_())