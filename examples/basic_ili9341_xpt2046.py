"""Basic usage example for micropython-ili9341-xpt2046."""

from machine import Pin, SPI

from ili9341_xpt2046.display.display import Display, color565
from ili9341_xpt2046.display.drivers.ili9341 import ILI9341Driver
from ili9341_xpt2046.input.touch import TouchInput
from ili9341_xpt2046.input.xpt2046 import XPT2046Touch


# ILI9341 SPI bus
hspi = SPI(
    1,
    baudrate=40000000,
    sck=Pin(14),
    mosi=Pin(13),
    miso=Pin(12),
)

# XPT2046 SPI bus
tspi = SPI(
    2,
    baudrate=1000000,
    sck=Pin(25),
    mosi=Pin(32),
    miso=Pin(39),
)


def on_touch(x, y):
    touch_queue.push(x, y)


driver = ILI9341Driver(
    hspi,
    cs=Pin(15, Pin.OUT),
    dc=Pin(2, Pin.OUT),
    rst=Pin(27, Pin.OUT),
    width=240,
    height=320,
    rotation=270,
)

display = Display(driver)

touch_queue = TouchInput()

touch = XPT2046Touch(
    tspi,
    cs=Pin(33, Pin.OUT),
    int_pin=Pin(36),
    int_handler=on_touch,
    width=240,
    height=320,
    invert_x=True,
)

WHITE = color565(255, 255, 255)
BLACK = color565(0, 0, 0)
GREEN = color565(0, 255, 0)

display.clear(BLACK)
display.draw_text(10, 10, "micropython-ili9341-xpt2046", WHITE)
display.draw_rect(10, 40, 220, 120, GREEN)

while True:
    point = touch_queue.touches()
    if point is None:
        continue

    x, y = point
    display.fill_circle(x, y, 3, WHITE)
