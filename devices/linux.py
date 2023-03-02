import utils
from block_device import BlockDevice

BLKGETSIZE64 = 0x80081272

class LinuxBlockDevice(BlockDevice):
    def __init__(self, path) -> None:
        if not utils.unix_is_block_device(path):
            raise ValueError(f"'{path}' is not a block device")
        self.path = path
    
    def get_size(self) -> bytes:
       with open(self.path, "rb") as f:
            return f.seek(0, 2)