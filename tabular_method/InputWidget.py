import sys

from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from qtpy import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PIWidget import PIWidget
from Minterm import Minterm

class InputWidget(QWidget):

    def __init__(self, parent=None):
        super(InputWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.resize(600, 400)
        vLayout = QVBoxLayout()

        label1 = QLabel("값을 입력해주세요")
        label2 = QLabel("값은 ,로 구분됩니다")
        label1.setAlignment(Qt.AlignCenter)
        label2.setAlignment(Qt.AlignCenter)

        label1.setFont(QtGui.QFont("Arial Rounded MT Bold", 20))
        label2.setFont(QtGui.QFont("Arial Rounded MT Bold", 10))

        hLayout1 = QHBoxLayout()
        mLabel = QLabel("minterm : ")
        self.mEdit = QLineEdit("1,2,3,4,5")

        hLayout1.addWidget(mLabel)
        hLayout1.addWidget(self.mEdit)

        hLayout2 = QHBoxLayout()
        dLabel = QLabel("don' care :" )
        self.dEdit = QLineEdit("6,7")

        hLayout2.addWidget(dLabel)
        hLayout2.addWidget(self.dEdit)


        nextBtn = QPushButton("입력")
        nextBtn.clicked.connect(self.next_btn_clicked)

        vLayout.addWidget(label1)
        vLayout.addWidget(label2)
        vLayout.setSpacing(1)
        vLayout.addLayout(hLayout1)
        vLayout.addLayout(hLayout2)
        vLayout.addSpacing(3)
        vLayout.addWidget(nextBtn)

        self.setLayout(vLayout)

    def next_btn_clicked(self):
        # todo : 유효성검사

        if self.mEdit.text() == '':
            QMessageBox.information(
                self, '알림', "값을 입력해주세요!",
                QMessageBox.Yes)
            return
        m = self.mEdit.text().split(',')
        d = self.dEdit.text().split(',')

        data =[]
        for i in range(len(m)):
            # Minterm, isDontCare, isCombined
            data.append([Minterm([int(m[i])]),True, False])

        for i in range(len(d)):
            data.append([Minterm([int(d[i])]),False, False])

        data = sorted(data, key=lambda x: x[0].num1)

        self.thisWindow = PIWidget(data,m,d)
        self.thisWindow.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InputWidget()
    ex.show()
    sys.exit(app.exec_())
