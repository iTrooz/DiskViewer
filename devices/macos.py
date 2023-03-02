import fcntl
import struct

import utils
from block_device import BlockDevice

DKIOCGETBLOCKSIZE  = 0x40046418
DKIOCGETBLOCKCOUNT = 0x40086419

"""
Source for getting block device size in MacOS :
https://blog.lnx.cx/2023/02/04/querying-block-device-sizes-in-python-on-linux-and-mac-os-x/
https://github.com/benschweizer/iops/blob/0977775ca01713fe2f13bbd8cf298054e3d879da/iops#L74
"""

class MacOSBlockDevice(BlockDevice):
    def __init__(self, _path) -> None:
        if not utils.unix_is_block_device(_path):
            raise ValueError(f"'{_path}' is not a block device")
        self._path = _path
    
    def get_path(self) -> str:
        return self._path
    
    def get_size(self) -> bytes:
        with open(self._path) as dev:

            buf = ' ' * 4
            buf = fcntl.ioctl(dev.fileno(), DKIOCGETBLOCKSIZE, buf)
            blockSize = struct.unpack('I', buf)[0]

            buf = ' ' * 8
            buf = fcntl.ioctl(dev.fileno(), DKIOCGETBLOCKCOUNT, buf)
            blockCount = struct.unpack('Q', buf)[0]

            return blockSize * blockCount
