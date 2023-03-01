import sys
import signal
import os
from enum import Enum
import stat

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from backends.ones_and_zeros import OnesAndZeros
from backends.ones_and_zeros_avg import OnesAndZerosAvg
from backends.byte_color import ByteColor

from block_device import BlockDevice

# Allow Ctrl+C
signal.signal(signal.SIGINT, signal.SIG_DFL)

class BackendType(Enum):
    ONES_AND_ZEROS = ("Ones and zeros", OnesAndZeros)
    ONES_AND_ZEROS_AVG = ("Ones and zeros average", OnesAndZerosAvg)
    BYTE_COLOR = ("Byte color", ByteColor)

    
    def __init__(self, text, class_):
        self.text = text
        self.class_ = class_


class MyApplication(QApplication):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.device = None
        self.backend = None

        self.CELL_HEIGHT_N = 16
        self.CELL_WIDTH_N = 50
        self.CELL_SIZE = 10

    def reloadTable(self):
        if not (self.backend and self.device):
            return

    def changeBackend(self):
        self.backend = list(BackendType)[self.backendComboBox.currentIndex()]
        self.reloadTable()

    def __is_block_device(self, path):
        if not os.path.exists(path):
            return False
        stats = os.stat(path)
        return stat.S_ISBLK(stats.st_mode)

    def changeDevice(self):
        device_path = self.deviceLineEdit.text()
        if self.device and self.device.path == device_path:
            return
        if not self.__is_block_device(device_path):
            print(f"{device_path} is not a valid block device")
            return

        self.device = BlockDevice(device_path)
        self.reloadTable()
        
    def init(self):
        self.init_ui()
        self.changeBackend()

    def init_ui(self):
        self.window = QWidget()
        self.window.setWindowTitle('Disk viewer')
        
        layout = QVBoxLayout()
        self.window.setLayout(layout)

        self.deviceLineEdit = QLineEdit()
        self.deviceLineEdit.editingFinished.connect(self.changeDevice)
        layout.addWidget(self.deviceLineEdit)

        self.backendComboBox = QComboBox()
        for inst in BackendType:
            self.backendComboBox.addItem(inst.text)
        
        self.backendComboBox.currentIndexChanged.connect(self.changeBackend)
        
        layout.addWidget(self.backendComboBox)

        self.table = QTableWidget(self.CELL_HEIGHT_N, self.CELL_WIDTH_N)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.table.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        for header in (self.table.horizontalHeader(), self.table.verticalHeader()):
            header.hide()
            header.setMinimumSectionSize(self.CELL_SIZE)
            header.setDefaultSectionSize(self.CELL_SIZE)
            header.setMaximumSectionSize(self.CELL_SIZE)

        # for some reason you need to do +5
        self.table.setFixedHeight(self.CELL_SIZE * self.CELL_HEIGHT_N + 5)
        self.table.setFixedWidth(self.CELL_SIZE * self.CELL_WIDTH_N + 5)

        layout.addWidget(self.table)

    def run(self):
        self.window.show()
        sys.exit(self.exec_())


app = MyApplication(sys.argv)
app.init()
app.run()

