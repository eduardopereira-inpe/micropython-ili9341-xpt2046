"""Bitmap blit helpers."""


class BlitMixin:
    """Draw RGB565 bitmap data."""

    def draw_bitmap(self, x, y, bitmap, w, h):
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)

        if w <= 0 or h <= 0:
            return

        x1 = x + w - 1
        y1 = y + h - 1

        if x1 < 0 or y1 < 0 or x >= self.width or y >= self.height:
            return

        if self._clip is None and x >= 0 and y >= 0 and x1 < self.width and y1 < self.height:
            self.block(x, y, x1, y1, bitmap)
            return

        # Fallback path for clipping or partially off-screen blits.
        stride = w * 2
        row_buf = bytearray(stride)

        for row in range(h):
            py = y + row
            if py < 0 or py >= self.height:
                continue

            src = row * stride
            row_buf[:] = bitmap[src:src + stride]

            for col in range(w):
                px = x + col
                if self._can_draw(px, py):
                    i = col * 2
                    color = (row_buf[i] << 8) | row_buf[i + 1]
                    self.draw_pixel(px, py, color)
