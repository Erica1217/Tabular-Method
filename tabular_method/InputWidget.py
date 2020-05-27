import sys

from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from qtpy import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PIWidget import PIWidget

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
        mEdit = QLineEdit("1,2,3,4,5")

        hLayout1.addWidget(mLabel)
        hLayout1.addWidget(mEdit)

        hLayout2 = QHBoxLayout()
        dLabel = QLabel("don' care :" )
        dEdit = QLineEdit("6,7")

        hLayout2.addWidget(dLabel)
        hLayout2.addWidget(dEdit)


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
        self.thisWindow = PIWidget()
        self.thisWindow.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InputWidget()
    ex.show()
    sys.exit(app.exec_())
