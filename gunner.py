import random

from pygame import Vector2

import u
from missile import Missile
from ship import Ship
from shot_optimizer import ShotOptimizer
from timer import Timer


class Gunner:
    def __init__(self, saucer_radius=20):
        self._missile_head_start = 2 * saucer_radius
        self._timer = Timer(u.SAUCER_MISSILE_DELAY)
        self._saucer_radius = saucer_radius

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
            self.create_random_missile(fleets, saucer)

    @staticmethod
    def should_target(chance, saucer):
        return saucer.always_target or chance < u.SAUCER_TARGETING_FRACTION

    def create_random_missile(self, fleets, saucer):
        target = self.random_position()
        self.create_unoptimized_missile(saucer.position, target, fleets)

    @staticmethod
    def create_optimal_missile(fleets, saucer, ship):
        target_solution = ShotOptimizer(saucer, ship)
        fleets.append(Missile.from_saucer(target_solution.start, target_solution.velocity))

    def create_unoptimized_missile(self, shooter_position, target_position, fleets):
        direction_to_target = (target_position - shooter_position).normalize()
        safety_offset = direction_to_target * self._missile_head_start
        velocity = direction_to_target * u.MISSILE_SPEED
        start = shooter_position + safety_offset

        missile = Missile.from_saucer(start, velocity)
        fleets.append(missile)

    @staticmethod
    def angle_to_hit(best_aiming_point, saucer_position):
        return Vector2(0, 0).angle_to(best_aiming_point - saucer_position)

    def closest_aiming_point(self, shooter_position, target_position, wrap_size):
        nearest_x = self.nearest(shooter_position.x, target_position.x, wrap_size)
        nearest_y = self.nearest(shooter_position.y, target_position.y, wrap_size)
        return Vector2(nearest_x, nearest_y)

    @staticmethod
    def nearest(shooter_coord, target_coord, screen_size):
        #     Handy Diagram
        #  ______|______|______
        #   T      T---S++T
        # Central T is too far away.
        # We are to his right, so
        # we shoot toward the right!
        direct_distance = abs(target_coord - shooter_coord)
        if direct_distance <= screen_size / 2:
            return target_coord
        elif shooter_coord > target_coord:
            return target_coord + screen_size
        else:
            return target_coord - screen_size

    def random_position(self):
        return Vector2(self.random_coordinate(), self.random_coordinate())

    @staticmethod
    def random_coordinate():
        return random.randrange(0, u.SCREEN_SIZE)

