import random

from pygame import Vector2

import u
from timer import Timer


class Fragment():
    def __init__(self, angle=None):
        angle = angle if angle else random.randrange(360)
        self.velocity = Vector2(u.FRAGMENT_SPEED, 0).rotate(angle)
        self.timer = Timer(u.FRAGMENT_LIFETIME, self.timeout)

    def tick(self, delta_time, fragments, _fleets):
        self.timer.tick(delta_time, fragments)
        # self.move(delta_time)

    def timeout(self, fragments):
        fragments.remove(self)
