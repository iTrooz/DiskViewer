import utils
import fcntl
import struct

# for linux
BLKGETSIZE64       = 0x80081272
# for MacOS
DKIOCGETBLOCKSIZE  = 0x40046418
DKIOCGETBLOCKCOUNT = 0x40086419

"""
Source for getting block device size in MacOS :
https://blog.lnx.cx/2023/02/04/querying-block-device-sizes-in-python-on-linux-and-mac-os-x/
https://github.com/benschweizer/iops/blob/0977775ca01713fe2f13bbd8cf298054e3d879da/iops#L74
"""

class BlockDevice:
    def __init__(self, path) -> None:
        self.path = path

    def __str__(self) -> str:
        return f"BlockDevice({self.path})"
    
    def __repr__(self) -> str:
        return self.__str__()

    def get_bytes(self, offset, size) -> bytes:
        with open(self.path, "rb") as f:
            f.seek(offset, 0)
            return f.read(size)
    
    def get_size(self) -> bytes:
        match utils.get_platform():
            case utils.Plateform.LINUX:
                with open(self.path, "rb") as f:
                    return f.seek(0, 2)
            case utils.Plateform.MACOS:
                with open(self.path) as dev:
                    
                    buf = ' ' * 4
                    buf = fcntl.ioctl(dev.fileno(), DKIOCGETBLOCKSIZE, buf)
                    blockSize = struct.unpack('I', buf)[0]

                    buf = ' ' * 8
                    buf = fcntl.ioctl(dev.fileno(), DKIOCGETBLOCKCOUNT, buf)
                    blockCount = struct.unpack('Q', buf)[0]

                    return blockSize * blockCount
            case utils.Plateform.WINDOWS:
                raise NotImplementedError()
