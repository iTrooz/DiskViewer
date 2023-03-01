from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class OnesAndZeros:
    
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
            ones_count = format(byte, 'b').count('1')            
            color_comp = int(ones_count*256/8)

            item.setBackground(QBrush(QColor(color_comp, color_comp, color_comp)))


