import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class OnesAndZeros:
    
    def __init__(self, table, device, tableIndexes):
        self.table = table
        self.device = device
        self.tableIndexes = tableIndexes

    def run(self):
        for i,j in self.tableIndexes:
            item = QTableWidgetItem()
            item.setBackground(QBrush(Qt.red))
            self.table.setItem(i, j, item)
