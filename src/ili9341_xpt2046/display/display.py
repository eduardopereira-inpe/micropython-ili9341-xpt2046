"""High-level display API for micropython-ili9341-xpt2046."""

from .mixins import (
    BlitMixin,
    ClippingMixin,
    GeometryMixin,
    TextMixin,
    TransformMixin,
)


def color565(r, g, b):
    """Convert RGB888 to RGB565."""
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)


class Display(
    ClippingMixin,
    GeometryMixin,
    BlitMixin,
    TextMixin,
    TransformMixin,
):
    """Driver-agnostic drawing API backed by a concrete driver instance."""

    __slots__ = (
        "_driver",
        "width",
        "height",
        "_clip",
        "_background",
    )

    def __init__(self, driver):
        self._driver = driver
        self.width = int(driver.width)
        self.height = int(driver.height)
        self._clip = None
        self._background = None

    @property
    def driver(self):
        return self._driver

    def block(self, x0, y0, x1, y1, data):
        self._driver.block(x0, y0, x1, y1, data)

    def draw_pixel(self, x, y, color):
        if not self._can_draw(int(x), int(y)):
            return

        self._driver.draw_pixel(int(x), int(y), int(color))

    def clear(self, color=0x0000):
        self._driver.clear(int(color))

    def display_on(self):
        if hasattr(self._driver, "display_on"):
            self._driver.display_on()

    def display_off(self):
        if hasattr(self._driver, "display_off"):
            self._driver.display_off()

    def load_background(self, path):
        size = self.width * self.height * 2
        with open(path, "rb") as file:
            self._background = file.read(size)

    def draw_background(self):
        if self._background is None:
            return

        self.block(0, 0, self.width - 1, self.height - 1, self._background)

    def restore_background(self, x, y, w, h):
        if self._background is None:
            return

        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)

        if w <= 0 or h <= 0:
            return

        if x < 0:
            w += x
            x = 0

        if y < 0:
            h += y
            y = 0

        if x >= self.width or y >= self.height:
            return

        if x + w > self.width:
            w = self.width - x

        if y + h > self.height:
            h = self.height - y

        if w <= 0 or h <= 0:
            return

        line = self.width * 2
        out = bytearray(w * h * 2)

        pos = 0
        for row in range(h):
            src = ((y + row) * line) + (x * 2)
            size = w * 2
            out[pos:pos + size] = self._background[src:src + size]
            pos += size

        self.block(x, y, x + w - 1, y + h - 1, out)
