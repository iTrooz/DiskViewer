import re
from enum import Enum

import wmi

from block_device import BlockDevice

class DeviceType(Enum):
    PHYSICAL = 0
    LOGICAL = 1

class WindowsBlockDevice(BlockDevice):
    
    PHYSICAL_DISK_PAT = re.compile("^PhysicalDrive([0-9])+$")
    LOGICAL_DISK_PAT = re.compile("^([A-Za-z]:)$")

    def __init__(self, device_name) -> None:
        self.wmi = wmi.WMI()

        if pat_result := self.PHYSICAL_DISK_PAT.search(device_name):
            self._path = pat_result.group(1)
            devices = self.wmi.Win32_DiskDrive(Index=int(self._path))
            self.type = DeviceType.PHYSICAL
        elif pat_result := self.LOGICAL_DISK_PAT.search(device_name):
            self._path = pat_result.group(1)
            devices = self.wmi.Win32_LogicalDisk(Name=self._path)
            self.type = DeviceType.LOGICAL
        else:
            raise ValueError(f"'{device_name}' is not a physical or logical device")
            
        if len(devices) != 1:
            raise ValueError(f"Invalid results for type {self.type.name} and argument {device_name}")
        self.device = devices[0]

    def get_path(self) -> str:
        match self.type:
            case DeviceType.PHYSICAL:
                return fr"\\.\PhysicalDrive{self._path}"
            case DeviceType.LOGICAL:
                return fr"\\.\{self._path}"
            case _:
                raise NotImplementedError()

    def get_size(self) -> bytes:
        return int(self.device.size)

    def get_bytes(self, offset, size) -> bytes:
        with open(self.get_path(), "rb") as f:
            
            # Windows wants us to align the offset
            alignment = self.device.BytesPerSector if self.type == DeviceType.PHYSICAL else 512
            aligned_offset = round(offset/alignment)*alignment
            
            f.seek(aligned_offset, 0)
            return f.read(size)
