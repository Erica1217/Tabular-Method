import sys

from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from qtpy import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PatrickWidget import PatrickWidget

class EPIWidget(QWidget):

    def __init__(self, data, mintermList, dontcareList):
        super(EPIWidget, self).__init__()
        self.data = data
        self.mintermList = mintermList
        self.dontcareList = dontcareList
        self.tableHeaderList = sorted(mintermList + dontcareList)
        self.isCoveredMintermList = [False for i in range(len(self.tableHeaderList))]
        self.isCoveredPIList = [False for i in range(len(self.data))]
        self.epiList=[]
        self.i
        self.epi_data = self.cvt_epi_data(data)
        self.status = 0 # 0:get_epi / 1:column_dominance / 2:row_dominance

        self.isFinished=False
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

        self.set_table(self.piTable1,self.data, self.epi_data)
        # self.set_table(self.piTable2,)

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
        if self.isFinished:
            self.thisWindow = PatrickWidget(self.data)
            self.thisWindow.show()
            return

        self.set_table(self.piTable1, self.data, self.epi_data)
        if self.status == 0:
            self.get_epi(self.epi_data)
            self.status=1
        elif self.status == 1:
            self.epi_data = self.check_column_dominance(self.epi_data)
            self.status = 2
        elif self.status == 2:
            self.epi_data=self.check_row_dominacnce(self.epi_data)
            self.status = 0

        self.set_table(self.piTable2, self.data, self.epi_data)

    def cvt_epi_data(self, data):
        result = []

        for i in range(len(data)):
            tmp = []
            for j in range(len(self.tableHeaderList)):
                if int(self.tableHeaderList[j]) in data[i][0].numbers:
                    tmp.append(1)
                else:
                    tmp.append(0)
            result.append(tmp)
        return result

    def set_table(self, table, data, epi_data):

        table.setColumnCount(len(self.tableHeaderList)+1)
        table.setRowCount(len(data)+1)
        table.setHorizontalHeaderLabels(self.tableHeaderList)

        table.setColumnWidth(0,60)
        for i in range(1,len(self.tableHeaderList)+1):
            table.setColumnWidth(i ,40)

        for i in range(len(data)):
            pi_item = QTableWidgetItem(data[i][0].binary)
            pi_item.setTextAlignment(Qt.AlignCenter)

            isCoverd = self.isCoveredPIList[i]

            table.setItem(i,0, pi_item)

            for j in range(len(epi_data[0])):
                isCoverd = isCoverd or self.isCoveredMintermList[j]
                item = QTableWidgetItem('v' if epi_data[i][j] else '')
                if isCoverd:
                    item.setBackground(QtGui.QColor(100,100,150))
                else:
                    item.setBackground(QtGui.QColor(255, 255, 255))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, j+1, item)

    def get_epi(self, currentData):
        for i in range(len(currentData[0])):
            count = sum(row[i] for row in currentData)
            if count == 1:
                for j in range(len(currentData)):
                    if currentData[j][i]== 1:
                        self.isCoveredMintermList[i]=True
                        self.isCoveredPIList[j]=True
                        currentData[j]=[0 for i in range(len(self.tableHeaderList))]
                        for k in range(len(self.data[j][0].numbers)):
                            idx = self.tableHeaderList.index(self.data[j][0].numbers[k])
                            self.isCoveredMintermList[idx] = True
                        self.epiList.append(self.data[j][0])
                        break

        return

    def check_column_dominance(self, currentData):
        result = currentData
        updateCover = []
        for i in range(len(currentData[0])):
            for j in range(len(currentData[0])):

                if not self.isCoveredMintermList[j] and i != j:
                    for k in range(len(currentData)):
                        if currentData[k][j] == 1 and currentData[k][i] == 0:
                            break
                    else:
                        print(i,j,"c d")
                        self.isCoveredMintermList[i] = True
                        updateCover.append(j)

        # for i in range(len(updateCover)):
        #     for j in range(len(currentData)):
        #         currentData[j][updateCover[i]] = 0
        return result

    def check_row_dominacnce(self, currentData):
        result = currentData
        updateCover = []
        for i in range(len(currentData)):
            for j in range(len(currentData)):

                if not self.isCoveredPIList[i] and not self.isCoveredPIList[j] and i != j:
                    for k in range(len(currentData[0])):
                        if currentData[j][k]==1 and currentData[i][k]==0:
                            break
                    else:
                        print(i,j,"rd")
                        self.isCoveredPIList[j] = True
                        updateCover.append(j)

        # emptyList = [0 for i in range(len(self.tableHeaderList))]
        # for i in range(len(updateCover)):
        #     currentData[updateCover[i]] = emptyList
        return result

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EPIWidget()
    ex.show()
    sys.exit(app.exec_())