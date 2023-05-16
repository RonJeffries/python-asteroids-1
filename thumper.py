

class Thumper:
    def __init__(self, b1, b2):
        self._long_interval = 30/60
        self._short_interval = 8/60
        self._decrement_interval = 127/60
        self.b1 = b1
        self.b2 = b2
        self.reset()

    # noinspection PyAttributeOutsideInit
    def reset(self):
        self._interval = self._long_interval
        self._decrement_time = 0
        self._execute_time = 0


    def tick(self, delta_time):
        self._execute_time += delta_time
        if self._execute_time >= self._interval:
            self._execute_time = 0
            self.b1()
            self.b1, self.b2 = self.b2, self.b1
        self._decrement_time += delta_time
        if self._decrement_time >= self._decrement_interval:
            self._decrement_time = 0
            self._interval = self._interval - 1/60
            if self._interval < 8/60:
                self._interval = 8/60