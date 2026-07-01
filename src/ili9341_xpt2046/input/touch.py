"""High-level touch queue and gesture helpers."""

try:
    import uasyncio as asyncio
except Exception:
    import asyncio


class TouchInput:
    """Touch queue with sync and async access."""

    __slots__ = ("_queue", "_event", "_last_tap")

    def __init__(self):
        self._queue = []
        self._event = asyncio.Event()
        self._last_tap = (-1, -1)

    @property
    def last_tap(self):
        return self._last_tap

    @last_tap.setter
    def last_tap(self, value):
        self._last_tap = (int(value[0]), int(value[1]))

    def push(self, x, y):
        self._queue.append((int(x), int(y)))
        try:
            self._event.set()
        except Exception:
            pass

    def touches(self):
        if self._queue:
            return self._queue.pop(0)

        return None

    async def wait_touch(self):
        while not self._queue:
            self._event.clear()
            await self._event.wait()

        return self._queue.pop(0)

    async def touch_stream(self):
        while True:
            yield await self.wait_touch()

    def double_tap(self, x, y, error_margin=10):
        lx, ly = self._last_tap

        if lx - error_margin <= x <= lx + error_margin:
            if ly - error_margin <= y <= ly + error_margin:
                self._last_tap = (-1, -1)
                return True

        self._last_tap = (int(x), int(y))
        return False
