from backends.abackend import ABackend

class OnesAndZeros(ABackend):

    def draw_pixel(self, i):
        byte = self.device.get_bytes(int(self.step*i), 1)[0]
        ones_count = format(byte, 'b').count('1')            
        color_comp = int(ones_count*256/8)

        return (color_comp, color_comp, color_comp)
