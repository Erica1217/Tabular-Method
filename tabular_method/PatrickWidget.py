import sys

from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from qtpy import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from ResultWidget import ResultWidget
from Monomial import Monomial

class PatrickWidget(QWidget):

    def __init__(self, data, uncoveredMinterm, NEPIList ,EPIList):
        super(PatrickWidget, self).__init__()
        self.data = data
        self.uncoveredMinterm = uncoveredMinterm
        self.EPIList = EPIList
        self.NEPIList = NEPIList

        self.init_ui()

    def init_ui(self):
        self.resize(1000, 400)
        vLayout = QVBoxLayout()
        titleLabel = QLabel("Petrick Method")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setFont(QtGui.QFont("Arial Rounded MT Bold", 20))

        hLayout = QHBoxLayout()

        beforeLabel = QLabel(self.cvt_mintermlist_to_str(self.NEPIList))
        resultLabel = QLabel(self.petrick_method())

        hLayout.addWidget(beforeLabel)
        hLayout.addWidget(resultLabel)

        self.nextBtn = QPushButton("next")
        self.nextBtn.setText("Finish")
        self.nextBtn.setStyleSheet("background-color: blue")
        self.nextBtn.clicked.connect(self.next_btn_clicked)

        vLayout.addWidget(titleLabel)
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.nextBtn)

        self.setLayout(vLayout)

    def cvt_mintermlist_to_str(self, lst):
        result=""
        for i in range(len(lst)):
            result+="("
            for j in range(len(lst[i])):
                result = result+lst[i][j].getName()
                if(j!=len(lst[i])-1):
                    result+="+"
            result+=")"

        result+="="
        return result

    def cvt_petricklist_to_str(self, lst):
        result=""
        for i in range(len(lst)):
            result+="("
            for j in range(len(lst[i])):
                result = result+lst[i][j]
                if(j!=len(lst[i])-1):
                    result+="*"

            if i != len(lst)-1:
                result+=")+"
            else:
                result+=")"

        return result

    def petrick_method(self):
        polynomial = []
        # todo nepi List length가 1이면 바로 리턴가능

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
                # 각 단항식에 추가

                for k in range(len(polynomial[i-1])):
                    s = set(list(polynomial[i-1][k])+[self.NEPIList[i][j].getName()])
                    p.append(s)
            polynomial.append(p)

        polynomial = polynomial[len(self.NEPIList)-1]
        deduplicate = set(map(lambda x: frozenset(x), polynomial))
        print(polynomial)
        print(deduplicate)
        print(len(polynomial), len(deduplicate))

        deduplicate = list(deduplicate)
        deduplicate.sort(key=lambda x : len(x))

        idx = 0
        while len(deduplicate)>idx:

            # subset 제거
            deleteList=[]
            for i in range(idx+1, len(deduplicate)):
                if deduplicate[idx].issubset(deduplicate[i]):
                    deleteList.append(deduplicate[i])
            # 삭제
            for i in range(len(deleteList)):
                deduplicate.remove(deleteList[i])

            idx += 1

        result =""

        # list[list[]] 형태로 변환
        deduplicate = list(map(lambda x:list(x), deduplicate))
        for i in range(len(deduplicate)):
            deduplicate[i].sort(key= lambda x: int(x[1:]))
            print(deduplicate[i])

        return self.cvt_petricklist_to_str(deduplicate)

    def next_btn_clicked(self):
        self.thisWindow = ResultWidget(self.data)
        self.thisWindow.show()
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PatrickWidget()
    ex.show()
    sys.exit(app.exec_())