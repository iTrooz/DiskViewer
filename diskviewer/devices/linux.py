from diskviewer import utils
from diskviewer.block_device import BlockDevice

BLKGETSIZE64 = 0x80081272

class LinuxBlockDevice(BlockDevice):
    def __init__(self, _path) -> None:
        if not utils.unix_is_block_device(_path):
            raise ValueError(f"'{_path}' is not a block device")
        self._path = _path

    def get_path(self) -> str:
        return self._path
    
    def get_size(self) -> bytes:
       with open(self._path, "rb") as f:
            return f.seek(0, 2)

    def get_bytes(self, offset, size) -> bytes:
        with open(self.get_path(), "rb") as f:
            f.seek(offset, 0)
            return f.read(size)
