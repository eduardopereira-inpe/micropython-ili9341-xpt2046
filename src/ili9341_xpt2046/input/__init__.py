"""Input package for micropython-ili9341-xpt2046."""

from .touch import TouchInput
from .xpt2046 import XPT2046Touch

__all__ = [
    "TouchInput",
    "XPT2046Touch",
]
