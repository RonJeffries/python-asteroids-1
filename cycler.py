

class Cycler:
    def __init__(self, values):
        self._values = values
        self._index = 0

    def next(self):
        next = self._values[self._index]
        self._index = (self._index + 1) % len(self._values)
        return next