"""Text drawing helpers."""

try:
    from framebuf import FrameBuffer, RGB565
except Exception:
    FrameBuffer = None
    RGB565 = None


class TextMixin:
    """Draw text with optional FrameBuffer acceleration."""

    def draw_text(self, x, y, text, color, bg=0x0000):
        if not text:
            return

        if FrameBuffer is None:
            # Fallback with visible placeholders when framebuf is unavailable.
            cursor = int(x)
            for _ in text:
                self.fill_rect(cursor, int(y), 6, 8, bg)
                self.draw_rect(cursor, int(y), 6, 8, color)
                cursor += 8
            return

        w = len(text) * 8
        h = 8
        buf = bytearray(w * h * 2)

        fbuf = FrameBuffer(buf, w, h, RGB565)
        if bg is not None:
            fbuf.fill(bg)

        fbuf.text(text, 0, 0, color)
        self.draw_bitmap(int(x), int(y), buf, w, h)
