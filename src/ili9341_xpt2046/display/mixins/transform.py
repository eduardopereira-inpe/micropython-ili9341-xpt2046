"""RGB565 transform helpers."""


class TransformMixin:
    """Flip and rotate RGB565 bitmaps."""

    def flip_bitmap(self, bitmap, w, h, flip_x=False, flip_y=False):
        if not (flip_x or flip_y):
            return bitmap

        w = int(w)
        h = int(h)
        dst = bytearray(len(bitmap))

        for y in range(h):
            sy = h - 1 - y if flip_y else y
            for x in range(w):
                sx = w - 1 - x if flip_x else x

                src_i = (sy * w + sx) * 2
                dst_i = (y * w + x) * 2

                dst[dst_i] = bitmap[src_i]
                dst[dst_i + 1] = bitmap[src_i + 1]

        return dst

    def draw_bitmap_transformed(self, x, y, bitmap, w, h, flip_x=False, flip_y=False):
        transformed = self.flip_bitmap(bitmap, w, h, flip_x=flip_x, flip_y=flip_y)
        self.draw_bitmap(x, y, transformed, w, h)
