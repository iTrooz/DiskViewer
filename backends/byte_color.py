from backends.abackend import ABackend

class ByteColor(ABackend):

    def draw_pixel(self, i):
        byte = self.device.get_bytes(int(self.step*i), 1)[0]
        
        red = (byte >> 6) & 0b111
        green = (byte >> 2) & 0b111
        blue = byte & 0b11

        red = int(red * 256 / 0b111)
        green = int(green * 256 / 0b111)
        blue = int(blue * 256 / 0b11)

        return (red, green, blue)
