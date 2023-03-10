from abc import ABC, abstractmethod

class ABackend(ABC):

    def __init__(self, table, device, tableIndexes, edit_table_sig):
        self.table = table
        self.device = device
        self.tableIndexes = tableIndexes
        self.edit_table_sig = edit_table_sig

    @abstractmethod
    def draw_pixel(x, y) -> tuple:
        pass

    def run(self, worker):
        self.step = self.device.get_size()/len(self.tableIndexes)
        for (x, y), i in zip(self.tableIndexes, range(len(self.tableIndexes))):
            if worker.cancelFlag:
                return

            ret = self.draw_pixel(i)

            self.edit_table_sig.emit((x, y, ret))
