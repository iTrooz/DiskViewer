from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ByteValue:
    
    def __init__(self, table, device, tableIndexes):
        self.table = table
        self.device = device
        self.tableIndexes = tableIndexes

    def run(self):
        step = self.device.get_size()/len(self.tableIndexes)
        for (x, y), i in zip(self.tableIndexes, range(len(self.tableIndexes))):
            item = QTableWidgetItem()
            self.table.setItem(x, y, item)

            byte = self.device.get_bytes(int(step*i), 1)[0]

            item.setBackground(QBrush(QColor(byte, byte, byte)))


