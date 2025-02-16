from diskviewer import utils

class BlockDevice:
    def __init__(self, path) -> None:
        raise RuntimeError("Use BlockDevice.create()")

    @staticmethod
    def create(path):
        return BlockDevice.get_class()(path)
    
    @staticmethod
    def get_class():
        match utils.get_platform():
            case utils.Platform.LINUX:
                from devices.linux import LinuxBlockDevice
                return LinuxBlockDevice
            case utils.Platform.MACOS:
                from devices.macos import MacOSBlockDevice
                return MacOSBlockDevice
            case utils.Platform.WINDOWS:
                from devices.windows import WindowsBlockDevice
                return WindowsBlockDevice
            case _:
                raise NotImplementedError()


    def __str__(self) -> str:
        return f"BlockDevice({self.get_path()})"
    
    def __repr__(self) -> str:
        return self.__str__()
