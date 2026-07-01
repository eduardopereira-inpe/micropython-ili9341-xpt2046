"""XPT2046 touch controller driver for micropython-ili9341-xpt2046."""

try:
    from micropython import const
except Exception:
    def const(value):
        return value

from machine import Pin


class XPT2046Touch:
    """Read and normalize coordinates from XPT2046 over SPI."""

    GET_X = const(0xD0)
    GET_Y = const(0x90)

    def __init__(
        self,
        spi,
        cs,
        width=240,
        height=320,
        x_min=100,
        x_max=1962,
        y_min=100,
        y_max=1900,
        invert_x=False,
        invert_y=False,
        rotation=0,
        int_pin=None,
        int_handler=None,
    ):
        self.spi = spi

        self.cs = cs
        self.cs.init(Pin.OUT, value=1)

        self.width = int(width)
        self.height = int(height)

        self.x_min = int(x_min)
        self.x_max = int(x_max)
        self.y_min = int(y_min)
        self.y_max = int(y_max)

        self.invert_x = bool(invert_x)
        self.invert_y = bool(invert_y)
        self.rotation = int(rotation)

        self.x_multiplier = self.width / (self.x_max - self.x_min)
        self.x_add = -self.x_min * self.x_multiplier

        self.y_multiplier = self.height / (self.y_max - self.y_min)
        self.y_add = -self.y_min * self.y_multiplier

        self.rx_buf = bytearray(3)
        self.tx_buf = bytearray(3)

        self.int_handler = int_handler
        self.int_pin = None

        if int_pin is not None:
            self.int_pin = int_pin
            self.int_pin.init(Pin.IN)
            self.int_pin.irq(trigger=Pin.IRQ_FALLING, handler=self._irq)

    @property
    def touched(self):
        if self.int_pin is None:
            return False

        return self.int_pin.value() == 0

    def _irq(self, _pin):
        if self.int_handler is None:
            return

        point = self.get_touch()
        if point is None:
            return

        try:
            self.int_handler(*point)
        except Exception:
            pass

    def normalize(self, x, y):
        x = int(self.x_multiplier * x + self.x_add)
        y = int(self.y_multiplier * y + self.y_add)

        if self.invert_x:
            x = self.width - 1 - x

        if self.invert_y:
            y = self.height - 1 - y

        if self.rotation == 0:
            return x, y

        if self.rotation == 90:
            return y, self.width - 1 - x

        if self.rotation == 180:
            return self.width - 1 - x, self.height - 1 - y

        if self.rotation == 270:
            return self.height - 1 - y, x

        return x, y

    def raw_touch(self):
        x = self.send_command(self.GET_X)
        y = self.send_command(self.GET_Y)

        if self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max:
            return x, y

        return None

    def get_touch(self, samples=5):
        xs = []
        ys = []

        for _ in range(samples):
            value = self.raw_touch()
            if value is None:
                return None

            xs.append(value[0])
            ys.append(value[1])

        xs.sort()
        ys.sort()

        xs = xs[1:-1]
        ys = ys[1:-1]

        mean_x = sum(xs) // len(xs)
        mean_y = sum(ys) // len(ys)

        return self.normalize(mean_x, mean_y)

    def send_command(self, command):
        self.tx_buf[0] = command

        self.cs(0)
        self.spi.write_readinto(self.tx_buf, self.rx_buf)
        self.cs(1)

        return (self.rx_buf[1] << 4) | (self.rx_buf[2] >> 4)
