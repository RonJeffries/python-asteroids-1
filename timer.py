# Timer
from typing import Callable, Union


class Timer:
    def __init__(self, delay):
        """action is callable returning None or bool"""
        self.delay = delay
        self.action = self.call_back
        self.elapsed = 0

    def tick(self, delta_time, *tick_args):
        self.elapsed += delta_time
        if self.elapsed >= self.delay:
            action = self.call_back
            action_complete = action(*tick_args)
            if action_complete is None or action_complete:
                self.elapsed = 0

    @staticmethod
    def call_back(action: Callable[[...], Union[None, bool]], *args):
        return action(*args)


