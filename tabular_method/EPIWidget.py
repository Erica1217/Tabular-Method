import sys

from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from qtpy import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PatrickWidget import PatrickWidget
from ResultWidget import ResultWidget

class EPIWidget(QWidget):

    def __init__(self, data, mintermList, dontcareList):
        super(EPIWidget, self).__init__()
        self.data = data
        self.mintermList = mintermList
        self.dontcareList = dontcareList
        self.tableHeaderList = sorted(mintermList + dontcareList, key=int)
        self.isCoveredMintermList = [False for i in range(len(self.tableHeaderList))]
        # 0 : 커버되지 않음, 1 : epi, 2: epi 아님
        self.isCoveredPIList = [0 for i in range(len(self.data))]
        self.epiList=[]
        self.epi_real_data = self.cvt_epi_data(data) # 계산하기위해 저장(값이 계속 바뀜)
        self.epi_table_data = self.cvt_epi_data(data) # 테이블로 보여주기위해 저장
        self.status = 0 # 0:get_epi / 1:column_dominance / 2:row_dominance

        self.isFinished=False
        self.isChanged=True
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

        self.set_table(self.piTable1,self.data, self.epi_table_data)
        # self.set_table(self.piTable2,)

        nextLabel = QLabel("->")

        hLayout.addWidget(self.piTable1)
        hLayout.addWidget(nextLabel)
        hLayout.addWidget(self.piTable2)

        self.nextBtn = QPushButton("다음")
        self.nextBtn.clicked.connect(self.next_btn_clicked)

        self.epiListView = QTableWidget()
        self.set_epilist_table(self.epiListView)

        vLayout.addWidget(titleLabel)
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.epiListView)
        vLayout.addWidget(self.nextBtn)

        self.setLayout(vLayout)

    def next_btn_clicked(self):
        if self.isFinished:
            self.thisWindow = ResultWidget(self.data)
            self.thisWindow.show()
            return

        self.set_table(self.piTable1, self.data, self.epi_table_data)
        if self.status == 0:
            self.isChanged = False
            self.get_epi(self.epi_real_data)
            self.status=1

        elif self.status == 1:
            self.epi_real_data = self.check_column_dominance(self.epi_real_data)
            self.status = 2

        elif self.status == 2:
            self.epi_real_data=self.check_row_dominacnce(self.epi_real_data)
            self.status = 0

            if not self.isChanged:
                uncoverdMintermList=[]
                NEPIList=[]

                # 커버해야하는 minterm들을 체크
                for i in range(len(self.isCoveredMintermList)):
                    if not self.isCoveredMintermList[i] and self.tableHeaderList[i] not in self.dontcareList:

                        # 해당 minterm이 어떤 pi에 커버되는지 체크
                        mintermList=[]
                        for j in range(len(self.data)):
                            if self.isCoveredPIList[j]==0 and int(self.tableHeaderList[i]) in self.data[j][0].numbers:
                                mintermList.append(self.data[j][0])

                        uncoverdMintermList.append(self.tableHeaderList[i])
                        NEPIList.append(mintermList)

                self.thisWindow = PatrickWidget(self.data, uncoverdMintermList, NEPIList)
                self.thisWindow.show()
                return

        self.isFinished = True

        for i in range(len(self.isCoveredMintermList)):
            if not self.isCoveredMintermList[i] and self.tableHeaderList[i] not in self.dontcareList :
                self.isFinished = False
                break

        self.set_table(self.piTable2, self.data, self.epi_table_data)
        self.set_epilist_table(self.epiListView)

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

    def set_epilist_table(self, table):
        table.setColumnCount(1)
        table.setRowCount(len(self.epiList))
        table.setColumnWidth(0,150)
        table.setHorizontalHeaderLabels(["EPI List"])
        for i in range(len(self.epiList)):
            # item = QTableWidgetItem(str(self.epiList[i][0]))
            # table.setItem(i,0,QTableWidgetItem())
            table.setItem(i,0,QTableWidgetItem(self.epiList[i][0].getName()+" = "+str(self.epiList[i][0])))


    def set_table(self, table, data, epi_data):
        table.setColumnCount(len(self.tableHeaderList)+1)
        table.setRowCount(len(data)+1)
        table.setHorizontalHeaderLabels([""]+self.tableHeaderList)

        table.setColumnWidth(0, 90)
        for i in range(1, len(self.tableHeaderList) + 1):
            table.setColumnWidth(i, 40)

        for i in range(0,len(data)):
            pi_item = QTableWidgetItem( data[i][0].getName()+ " = " + data[i][0].binary)
            pi_item.setTextAlignment(Qt.AlignCenter)

            isEPI = self.isCoveredPIList[i] == 1

            table.setItem(i,0, pi_item)

            for j in range(len(epi_data[0])):
                item = QTableWidgetItem('v' if epi_data[i][j] else '')
                # EPI이면 노랑색으로 표시
                if isEPI:
                    item.setBackground(QtGui.QColor(255, 250, 205))
                # epi가 아닌 cover된 것이나 dominate되는 것들은 회색으로 표시
                elif self.isCoveredMintermList[j] or self.isCoveredPIList[i] == 2:
                    item.setBackground(QtGui.QColor(100,100,150))

                # 아직 cover되지 않은 것은 흰 색으로 표시
                else:
                    item.setBackground(QtGui.QColor(255, 255, 255))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, j+1, item)

    def get_epi(self, currentData):
        for i in range(len(currentData[0])):
            count = sum(row[i] for row in currentData)
            if count == 1: # column count가 1이면
                for j in range(len(currentData)):
                    self.isChanged=True
                    #  column count가 1인 minterm을 포함하는 PI를 찾음
                    if currentData[j][i] == 1:
                        self.isCoveredMintermList[i]=True
                        self.isCoveredPIList[j] = 1 # epi 찾음
                        currentData[j]=[0 for i in range(len(self.tableHeaderList))] # 0으로 초기화

                        #  해당 PI가 가지고 있는 minterm들도 모두 cover된 것으로 체크
                        for k in range(len(self.data[j][0].numbers)):
                            idx = self.tableHeaderList.index(str(self.data[j][0].numbers[k]))
                            self.isCoveredMintermList[idx] = True
                        self.epiList.append(self.data[j])
                        break

        return

    def check_column_dominance(self, currentData):
        result = currentData
        updateCover = []
        for i in range(len(currentData[0])):
            for j in range(len(currentData[0])):

                if not self.isCoveredMintermList[j] and i != j: #
                    for k in range(len(currentData)):
                        if currentData[k][j] == 1 and currentData[k][i] == 0:
                            break
                    else: #j가 superset
                        self.isCoveredMintermList[i] = True
                        updateCover.append(i)
                        self.isChanged=True


        for i in range(len(updateCover)):
            for j in range(len(currentData)):
                currentData[j][updateCover[i]] = 0
        return result

    def check_row_dominacnce(self, currentData):
        result = currentData
        updateCover = []
        for i in range(len(currentData)):
            for j in range(len(currentData)):

                if self.isCoveredPIList[i] == 0 and self.isCoveredPIList[j] == 0 and i != j:
                    for k in range(len(currentData[0])):
                        if currentData[j][k]==1 and currentData[i][k]==0:
                            break
                    else:
                        # print(i,j,"rd")
                        self.isCoveredPIList[j] = 2
                        updateCover.append(j)
                        self.isChanged = True

        emptyList = [0 for i in range(len(self.tableHeaderList))]
        for i in range(len(updateCover)):
            currentData[updateCover[i]] = emptyList
        return result

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EPIWidget()
    ex.show()
    sys.exit(app.exec_())