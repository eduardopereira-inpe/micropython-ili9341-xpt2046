"""Text drawing helpers."""

try:
    from framebuf import FrameBuffer, RGB565
except Exception:
    FrameBuffer = None
    RGB565 = None


class TextMixin:
    """Draw text with optional FrameBuffer acceleration."""

    VALID_ROTATIONS = (0, 90, 180, 270)

    def _text_flip_for_rotation(self):
        rotation = int(getattr(self, "rotation", 0))
        if rotation not in self.VALID_ROTATIONS:
            raise ValueError("rotation must be one of 0, 90, 180, 270")

        # For ILI9341 MADCTL setup used here, 180-degree mode mirrors glyphs
        # unless we horizontally flip the rendered text bitmap.
        if rotation == 180:
            return True, False

        return False, False

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

        flip_x, flip_y = self._text_flip_for_rotation()
        if flip_x or flip_y:
            self.draw_bitmap_transformed(int(x), int(y), buf, w, h, flip_x=flip_x, flip_y=flip_y)
            return

        self.draw_bitmap(int(x), int(y), buf, w, h)
