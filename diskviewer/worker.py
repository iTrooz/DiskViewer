from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Worker(QObject):

    def __init__(self, edit_table_sig, tableIndexes):
        super().__init__()
        self.edit_table_sig = edit_table_sig
        self.tableIndexes = tableIndexes

        self.mutex = QMutex()
        self.cancelFlag = False
    
    @pyqtSlot(tuple)
    def loadTable(self, backend_tuple):
        self.mutex.lock()
        
        backend = backend_tuple[0]
        self.cancelFlag = False
        backend.run(self)
        
        self.mutex.unlock()
