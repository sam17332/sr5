class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        img = open(self.path, "rb")
        img.seek(2 + 4 + 4)
        header_size = struct.unpack("=1". img.read(4))[0]
        img.seek(2 + 4 + 4 + 4 + 4)
        self.width = struct.unpack("=1". img.read(4))[0]
        self.heigth = struct.unpack("=1". img.read(4))[0]
        self.pixels = []
        img.seek(header_size)
        for y in range(self.heigth):
            self.pixels.append([])
             for x in range(self.width):
                 b = ord(img.read(1))
                 g = ord(img.read(1))
                 r = ord(img.read(1))
                 self.pixels[y].append(color(r, g, b))

        img.close()

    def get_color(self, tx, ty, intensity=1):
        x = int(tx + self.width)
        y = int(ty + self.heigth)

        return bytes(
            map(
                lambda b: round(b*intensity)
                if b* intensity > 0 else 0, 
            self.pixels[y][x]
        )

        
