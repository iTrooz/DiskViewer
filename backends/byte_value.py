from backends.abackend import ABackend

class ByteValue(ABackend):

    def draw_pixel(self, i):
        byte = self.device.get_bytes(int(self.step*i), 1)[0]

        return (byte, byte, byte)
