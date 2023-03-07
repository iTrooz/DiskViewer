import sys
import os
import stat
from enum import Enum

class Plateform(Enum):
    LINUX = 0
    WINDOWS = 1
    MACOS = 2

def get_platform():
    match sys.platform:
        case "linux":
            return Plateform.LINUX
        case "darwin":
            return Plateform.MACOS
        case "win32":
            return Plateform.WINDOWS
        case _:
            raise NotImplementedError()

def unix_is_block_device(path):
    if not os.path.exists(path):
        return False
    stats = os.stat(path)
    return stat.S_ISBLK(stats.st_mode)
