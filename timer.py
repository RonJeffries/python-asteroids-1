# Timer
from typing import Callable, Union


class Timer:
    def __init__(self, delay):
        self.delay = delay
        self.elapsed = 0

    def tick(self, delta_time, action: Callable[[...], Union[None, bool]], *args):
        self.elapsed += delta_time
        if self.elapsed >= self.delay:
            action_complete = action(*args)
            if action_complete is None or action_complete:
                self.elapsed = 0


