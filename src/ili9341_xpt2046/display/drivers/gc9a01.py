"""GC9A01 driver scaffold for micropython-ili9341-xpt2046."""

from time import sleep_ms

try:
    from micropython import const
except Exception:
    def const(value):
        return value


class GC9A01Driver:
    """Minimal GC9A01-compatible SPI driver scaffold."""

    SWRESET = const(0x01)
    SLPOUT = const(0x11)
    DISPLAY_ON = const(0x29)
    DISPLAY_OFF = const(0x28)
    SET_COLUMN = const(0x2A)
    SET_PAGE = const(0x2B)
    WRITE_RAM = const(0x2C)
    MADCTL = const(0x36)
    PIXFMT = const(0x3A)
    VALID_ROTATIONS = (0, 90, 180, 270)

    def __init__(self, spi, cs, dc, rst, width=240, height=240, rotation=0):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.width = int(width)
        self.height = int(height)

        rotation = int(rotation)
        if rotation not in self.VALID_ROTATIONS:
            raise ValueError("rotation must be one of 0, 90, 180, 270")

        self.rotation_degrees = rotation
        self.rotation = rotation

        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=1)

        self._reset()
        self._init_display()

    def _reset(self):
        self.rst(0)
        sleep_ms(50)
        self.rst(1)
        sleep_ms(50)

    def _init_display(self):
        self.write_cmd(self.SWRESET)
        sleep_ms(120)
        self.write_cmd(self.MADCTL, 0x00)
        self.write_cmd(self.PIXFMT, 0x55)
        self.write_cmd(self.SLPOUT)
        sleep_ms(120)
        self.write_cmd(self.DISPLAY_ON)

    def write_cmd(self, command, *args):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)

        if args:
            self.write_data(bytearray(args))

    def write_data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def block(self, x0, y0, x1, y1, data):
        self.write_cmd(self.SET_COLUMN, x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF)
        self.write_cmd(self.SET_PAGE, y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF)
        self.write_cmd(self.WRITE_RAM)
        self.write_data(data)

    def draw_pixel(self, x, y, color):
        self.block(x, y, x, y, int(color).to_bytes(2, "big"))

    def clear(self, color=0x0000):
        line = int(color).to_bytes(2, "big") * self.width
        for y in range(self.height):
            self.block(0, y, self.width - 1, y, line)

    def display_on(self):
        self.write_cmd(self.DISPLAY_ON)

    def display_off(self):
        self.write_cmd(self.DISPLAY_OFF)
