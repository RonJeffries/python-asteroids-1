import random

from pygame import Vector2

import u
from ship import Ship
from shot_optimizer import ShotOptimizer
from timer import Timer


class Gunner:
    def __init__(self, always_target):
        self._always_target = always_target
        self._timer = Timer(u.SAUCER_MISSILE_DELAY)

    def fire(self, delta_time, saucer, ship_or_none: Ship | None, fleets):
        self._timer.tick(delta_time, self.fire_if_missile_available, saucer, ship_or_none, fleets)

    def fire_if_missile_available(self, saucer, ship_or_none, fleets):
        if did_we_fire := saucer.missile_tally < u.SAUCER_MISSILE_LIMIT:
            self.fire_available_missile(saucer, ship_or_none, fleets)
        return did_we_fire

    def fire_available_missile(self, saucer, ship_or_none, fleets):
        if ship_or_none and self.should_target():
            solution = ShotOptimizer(saucer, ship_or_none).targeted_solution
        else:
            solution = ShotOptimizer(saucer, ship_or_none).random_solution
        fleets.append(solution.saucer_missile())

    def should_target(self):
        return self._always_target or random.random() < u.SAUCER_TARGETING_FRACTION


