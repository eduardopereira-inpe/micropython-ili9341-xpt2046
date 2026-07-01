"""Basic geometry drawing routines."""


class GeometryMixin:
    """Primitive drawing using draw_pixel and block."""

    def draw_hline(self, x, y, w, color):
        if w <= 0:
            return

        for xx in range(x, x + w):
            if self._can_draw(xx, y):
                self.draw_pixel(xx, y, color)

    def draw_vline(self, x, y, h, color):
        if h <= 0:
            return

        for yy in range(y, y + h):
            if self._can_draw(x, yy):
                self.draw_pixel(x, yy, color)

    def draw_line(self, x0, y0, x1, y1, color):
        x0 = int(x0)
        y0 = int(y0)
        x1 = int(x1)
        y1 = int(y1)

        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        err = dx + dy

        while True:
            if self._can_draw(x0, y0):
                self.draw_pixel(x0, y0, color)

            if x0 == x1 and y0 == y1:
                break

            e2 = err << 1
            if e2 >= dy:
                err += dy
                x0 += sx

            if e2 <= dx:
                err += dx
                y0 += sy

    def draw_rect(self, x, y, w, h, color):
        if w <= 0 or h <= 0:
            return

        self.draw_hline(x, y, w, color)
        self.draw_hline(x, y + h - 1, w, color)
        self.draw_vline(x, y, h, color)
        self.draw_vline(x + w - 1, y, h, color)

    def fill_rect(self, x, y, w, h, color):
        if w <= 0 or h <= 0:
            return

        for yy in range(y, y + h):
            self.draw_hline(x, yy, w, color)

    def draw_circle(self, x0, y0, r, color):
        if r <= 0:
            return

        x = r
        y = 0
        err = 0

        while x >= y:
            points = (
                (x0 + x, y0 + y),
                (x0 + y, y0 + x),
                (x0 - y, y0 + x),
                (x0 - x, y0 + y),
                (x0 - x, y0 - y),
                (x0 - y, y0 - x),
                (x0 + y, y0 - x),
                (x0 + x, y0 - y),
            )

            for px, py in points:
                if self._can_draw(px, py):
                    self.draw_pixel(px, py, color)

            y += 1
            if err <= 0:
                err += (y << 1) + 1
            if err > 0:
                x -= 1
                err -= (x << 1) + 1

    def fill_circle(self, x0, y0, r, color):
        if r <= 0:
            return

        for y in range(-r, r + 1):
            x_span = int((r * r - y * y) ** 0.5)
            self.draw_hline(x0 - x_span, y0 + y, (x_span << 1) + 1, color)
