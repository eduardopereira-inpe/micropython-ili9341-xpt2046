"""Clipping helpers for display composition."""


class ClippingMixin:
    """Adds optional clipping rectangle support."""

    __slots__ = ("_clip",)

    def set_clip(self, x, y, w, h):
        self._clip = (int(x), int(y), int(w), int(h))

    def clear_clip(self):
        self._clip = None

    def _in_clip(self, x, y):
        if self._clip is None:
            return True

        cx, cy, cw, ch = self._clip
        return cx <= x < (cx + cw) and cy <= y < (cy + ch)

    def _in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def _can_draw(self, x, y):
        return self._in_bounds(x, y) and self._in_clip(x, y)
