import socket

devices = []
deviceMap = {}


class ftdevice:
    def __init__(self, name, host, port=1337, width=45, height=35):
        self.name = name
        self.host = host
        self.port = port
        self.width = width
        self.height = height
        devices.append(self)
        deviceMap[name] = self

    def socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((self.host, self.port))
        return s


ftdevice("Flaschen Taschen", "ft.noise")
ftdevice("Noise Square Table", "square.noise", 1337, 810, 1)
# ftdevice("Bookshelves", "bookcase.noise", ...?)


class ftclient:
    def __init__(self, device=devices[0], layer=11, transparent=True):
        self.layer = layer
        self.s = device.socket()
        self.device = device
        self.genbuffer()
        self.transparent = transparent

    @property
    def width(self):
        return self.device.width

    @property
    def height(self):
        return self.device.height

    def genbuffer(self):
        b = "P6\n" + str(self.width) + " " + str(self.height) + "\n" + "255\n"
        a = "\n0\n0\n" + self.layer + "\n"
        pixels = self.width * self.height
        buf = bytearray(len(b)+3*pixels+len(a))
        self.buf = buf
        buf[0:len(b)] = b
        buf[-len(a):] = a
        self.offset = len(b)

    def setLayer(self, layer):
        self.layer = layer
        self.genbuffer()

    def set(self, color, x, y):
        (r, g, b) = color
        if r == 0 and g == 0 and b == 0 and not self.transparent:
            b = 1
        if r not in range(0, 256):
            raise ValueError("Red value not in [0,255]")
        if g not in range(0, 256):
            raise ValueError("Green value not in [0,255]")
        if b not in range(0, 256):
            raise ValueError("Blue value not in [0,255]")
        if x not in range(0, self.width):
            raise ValueError("x value outside if [0, width)")
        if y not in range(0, self.height):
            raise ValueError("y value outside if [0, height)")
        start = self.offset + (x + y * self.width)*3
        self.buf[start:start+3] = [r, g, b]

    def show(self):
        self.s.sendall(self.buf)


f = ftclient()
f.set(1, 1, [255, 255, 255])
f.show()
