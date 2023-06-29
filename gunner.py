import random

from pygame import Vector2

import u
from missile import Missile
from ship import Ship
from shot_optimizer import ShotOptimizer, FiringSolution
from timer import Timer


class Gunner:
    def __init__(self, saucer_radius=20):
        self._missile_head_start = 2 * saucer_radius
        self._timer = Timer(u.SAUCER_MISSILE_DELAY)

    def fire(self, delta_time, saucer, ship_or_none: Ship | None, fleets):
        self._timer.tick(delta_time, self.fire_if_missile_available, saucer, ship_or_none, fleets)

    def fire_if_missile_available(self, saucer, ship_or_none, fleets):
        if result := saucer.missile_tally < u.SAUCER_MISSILE_LIMIT:
            chance = random.random()
            self.fire_available_missile(chance, fleets, saucer, ship_or_none)
        return result

    def fire_available_missile(self, chance, fleets, saucer, ship_or_none):
        if ship_or_none and self.should_target(chance, saucer):
            self.create_optimal_missile(fleets, saucer, ship_or_none)
        else:
            self.create_random_missile(fleets, saucer, ship_or_none)

    @staticmethod
    def should_target(chance, saucer):
        return saucer.always_target or chance < u.SAUCER_TARGETING_FRACTION

    @staticmethod
    def create_random_missile(fleets, saucer, ship_or_none):
        solution = ShotOptimizer(saucer, ship_or_none).random_solution
        fleets.append(solution.saucer_missile())

    @staticmethod
    def create_optimal_missile(fleets, saucer, ship):
        solution = ShotOptimizer(saucer, ship).targeted_solution
        fleets.append(solution.saucer_missile())

