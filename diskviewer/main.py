import sys
import signal
import os
from enum import Enum
import stat
from concurrent.futures import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from diskviewer.backends.ones_and_zeros import OnesAndZeros
from diskviewer.backends.byte_value import ByteValue
from diskviewer.backends.byte_color import ByteColor

from diskviewer.block_device import BlockDevice
from diskviewer.worker import Worker

class BackendType(Enum):
    ONES_AND_ZEROS = ("Ones and zeros", OnesAndZeros)
    BYTE_VALUE = ("Byte value", ByteValue)
    BYTE_COLOR = ("Byte color", ByteColor)

    
    def __init__(self, text, class_):
        self.text = text
        self.class_ = class_


class MyApplication(QApplication):

    edit_table_sig = pyqtSignal(tuple)
    loadTable_sig = pyqtSignal(tuple)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.device = None
        self.backend = None

        # used to filter changeDevice()
        self.device_path = None

        self.CELL_HEIGHT_N = 16
        self.CELL_WIDTH_N = 50
        self.CELL_SIZE = 10
        
        self.workerThread = QThread(self)
        self.workerThread.start()

        self.worker = Worker(self.edit_table_sig, list(self.__tableIterator()))
        self.worker.moveToThread(self.workerThread)

        self.edit_table_sig.connect(self.edit_table)
        self.loadTable_sig.connect(self.worker.loadTable)

    def __tableIterator(self):
        for i in range(self.CELL_HEIGHT_N): 
            for j in range(self.CELL_WIDTH_N):
                yield i, j

    def reloadTable(self):
        if self.backend and self.device:

            # stop the old function call
            self.worker.cancelFlag = True

            # wait for the function to finish
            self.worker.mutex.lock()
            self.worker.mutex.unlock()

            # process all events in the queue (preparation to clear the table)
            QCoreApplication.processEvents()
            
            # clear the table
            for x, y in self.__tableIterator():
                self.edit_table((x, y, (255, 255, 255)))

            # start work
            backendInst = self.backend.class_(self.table, self.device, list(self.__tableIterator()), self.edit_table_sig)
            self.loadTable_sig.emit((backendInst,))

    @pyqtSlot(tuple)
    def edit_table(self, new_data):
        x,y, (r,g,b) = new_data
        item = QTableWidgetItem()
        item.setBackground(QBrush(QColor(r, g, b)))
        self.table.setItem(x, y, item)

    def changeBackend(self):
        self.backend = list(BackendType)[self.backendComboBox.currentIndex()]
        self.reloadTable()

    def changeDevice(self):
        device_path = self.deviceLineEdit.text()
        if self.device_path == device_path:
            return

        try:
            self.device = BlockDevice.create(device_path)
        except ValueError as e:
            print(str(e))
            return

        self.device_path = device_path
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

def main():
    # Allow Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = MyApplication(sys.argv)
    app.init()
    app.run()

if __name__ == '__main__':
    main()
