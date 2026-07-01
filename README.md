# micropython-ili9341-xpt2046

micropython-ili9341-xpt2046 is an independent MicroPython library for TFT display output and resistive touch input.

This repository provides:
- a high-level display API in src/ili9341_xpt2046/display/display.py,
- modular display drivers in src/ili9341_xpt2046/display/drivers,
- reusable drawing mixins in src/ili9341_xpt2046/display/mixins,
- touch input primitives in src/ili9341_xpt2046/input.

The project is designed to be reusable in different boards and applications, without coupling to CYDGUI.

## Repository Structure

- src/ili9341_xpt2046/display/display.py: high-level drawing API.
- src/ili9341_xpt2046/display/drivers/ili9341.py: ILI9341 SPI driver.
- src/ili9341_xpt2046/display/drivers/st7789.py: ST7789 scaffold driver.
- src/ili9341_xpt2046/display/drivers/gc9a01.py: GC9A01 scaffold driver.
- src/ili9341_xpt2046/display/mixins/geometry.py: lines, rectangles, circles.
- src/ili9341_xpt2046/display/mixins/blit.py: RGB565 bitmap drawing.
- src/ili9341_xpt2046/display/mixins/text.py: text drawing helpers.
- src/ili9341_xpt2046/display/mixins/clipping.py: clipping helpers.
- src/ili9341_xpt2046/display/mixins/transform.py: bitmap transforms.
- src/ili9341_xpt2046/input/xpt2046.py: XPT2046 touch driver.
- src/ili9341_xpt2046/input/touch.py: touch queue and double-tap helpers.
- examples/: usage examples.
- tests/: starter test area.

## Package Import

Use the package name with underscore:

from ili9341_xpt2046.display import Display
from ili9341_xpt2046.input.xpt2046 import XPT2046Touch

## MIP Installation

Typical install flow with MIP:

import mip

mip.install("github:<usuario>/micropython-ili9341-xpt2046")

## Quick Start

Example file:

- examples/basic_ili9341_xpt2046.py

Basic flow:

1. Create an SPI bus for display.
2. Create an ILI9341Driver.
3. Wrap it in Display.
4. Create an SPI bus for touch.
5. Create XPT2046Touch and send events into TouchInput.

## Status

- ILI9341 and XPT2046 are available in initial functional form.
- ST7789 and GC9A01 are included as initial scaffolds with common API.
- The architecture is ready for incremental optimization and feature expansion.

## License

MIT. See LICENSE.
