import utils

class BlockDevice:
    def __init__(self, path) -> None:
        raise RuntimeError("Use BlockDevice.create()")

    @staticmethod
    def create(path):
        return BlockDevice.get_class()(path)
    
    @staticmethod
    def get_class():
        match utils.get_platform():
            case utils.Plateform.LINUX:
                from devices.linux import LinuxBlockDevice
                return LinuxBlockDevice
            case utils.Plateform.MACOS:
                from devices.macos import MacOSBlockDevice
                return MacOSBlockDevice
            case utils.Plateform.WINDOWS:
                raise NotImplementedError()
            case _:
                raise NotImplementedError()


    def __str__(self) -> str:
        return f"BlockDevice({self.path})"
    
    def __repr__(self) -> str:
        return self.__str__()

    def get_bytes(self, offset, size) -> bytes:
        with open(self.path, "rb") as f:
            f.seek(offset, 0)
            return f.read(size)
