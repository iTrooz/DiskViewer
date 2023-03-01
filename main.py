import sys
import signal
from enum import Enum

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Allow Ctrl+C
signal.signal(signal.SIGINT, signal.SIG_DFL)

class BackendType(Enum):
    ONES_AND_ZEROS = "Ones and zeros"
    ONES_AND_ZEROS_AVG = "Ones and zeros average"
    BYTE_COLOR = "Byte color"

class MyApplication(QApplication):

    def changeBackend(self):
        inst = list(BackendType)[self.comboBox.currentIndex()]
        print(inst)
        
    def init(self):
        self.init_ui()
        self.changeBackend()

    def init_ui(self):
        self.window = QWidget()
        self.window.setWindowTitle('Disk viewer')
        
        layout = QVBoxLayout()
        self.window.setLayout(layout)

        self.comboBox = QComboBox()
        for inst in BackendType:
            self.comboBox.addItem(inst.value)
        
        self.comboBox.currentIndexChanged.connect(self.changeBackend)
        
        layout.addWidget(self.comboBox)

        CELL_HEIGHT_N = 16
        CELL_WIDTH_N = 50
        tableWidget = QTableWidget(CELL_HEIGHT_N, CELL_WIDTH_N)
        tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        tableWidget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        CELL_SIZE = 10
        for header in (tableWidget.horizontalHeader(), tableWidget.verticalHeader()):
            header.hide()
            header.setMinimumSectionSize(CELL_SIZE)
            header.setDefaultSectionSize(CELL_SIZE)
            header.setMaximumSectionSize(CELL_SIZE)

        # for some reason you need to do +5
        tableWidget.setFixedHeight(CELL_SIZE * CELL_HEIGHT_N + 5)
        tableWidget.setFixedWidth(CELL_SIZE * CELL_WIDTH_N + 5)

        layout.addWidget(tableWidget)

    def run(self):
        self.window.show()
        sys.exit(self.exec_())


app = MyApplication(sys.argv)
app.init()
app.run()

