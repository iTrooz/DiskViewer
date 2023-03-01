import sys
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