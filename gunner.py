from pygame import Vector2

import u
from missile import Missile
from timer import Timer


class Gunner:
    def __init__(self):
        self._timer = Timer(u.SAUCER_MISSILE_DELAY)

    def fire(self, delta_time, saucer_position, ship_position, fleets):
        self._timer.tick(delta_time, self.fire_missile, saucer_position, ship_position, fleets)

    def fire_missile(self, saucer_position, ship_position, fleets):
        fleets.add_flyer(Missile.from_saucer(saucer_position, Vector2(0, 0)))
