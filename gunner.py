import math
import random

from pygame import Vector2

import u
from missile import Missile
from ship import Ship
from timer import Timer


class Gunner:
    def __init__(self, saucer_radius=20):
        self._timer = Timer(u.SAUCER_MISSILE_DELAY)
        self._radius = saucer_radius

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

    def should_target(self, chance, saucer):
        return saucer.always_target or chance < u.SAUCER_TARGETING_FRACTION

    def create_random_missile(self, fleets, saucer):
        target = self.random_position()
        self.create_unoptimized_missile(saucer.position, target, fleets)

    def create_optimal_missile(self, fleets, saucer, ship):
        saucer_position = saucer.position
        closest_shot_position = self.closest_aiming_point(saucer_position, ship.position, u.SCREEN_SIZE)
        delta_position = closest_shot_position - saucer_position
        aim_time, adjustment_ratio = self.optimal_shot(delta_position, ship)
        target_position = closest_shot_position + ship.velocity * aim_time
        self.create_adjusted_missile(adjustment_ratio, target_position, saucer_position, fleets)

    def optimal_shot(self, delta_position, ship):
        aim_time = self.time_to_target(delta_position, ship.velocity)
        adjustment_ratio = self.compute_adjustment_ratio(aim_time)
        return aim_time, adjustment_ratio

    def compute_adjustment_ratio(self, aim_time):
        return self.compute_ratio(aim_time) if aim_time else 1

    def compute_ratio(self, aim_time):
        distance_to_target = aim_time * u.MISSILE_SPEED
        adjusted_distance = distance_to_target - 2 * self._radius
        return adjusted_distance / distance_to_target

    def create_adjusted_missile(self, adjustment_ratio, target_position, saucer_position, fleets):
        vector_to_target = target_position - saucer_position
        direction_to_target = vector_to_target.normalize()
        missile_velocity = u.MISSILE_SPEED * direction_to_target
        adjusted_velocity = missile_velocity * adjustment_ratio
        offset = 2 * self._radius * direction_to_target
        missile = Missile.from_saucer(saucer_position + offset, adjusted_velocity)
        fleets.append(missile)

    def time_to_target(self, delta_position, relative_velocity):
        # from https://www.gamedeveloper.com/programming/shooting-a-moving-target#close-modal
        # return time for hit or -1
        # quadratic
        a = relative_velocity.dot(relative_velocity) - u.MISSILE_SPEED*u.MISSILE_SPEED
        b = 2 * relative_velocity.dot(delta_position)
        c = delta_position.dot(delta_position)
        disc = b*b - 4*a*c
        if disc < 0:
            return 0
        else:
            divisor = (math.sqrt(disc) - b)
            if divisor:
                return 2*c / divisor
            else:
                return 0

    def create_unoptimized_missile(self, from_position, to_position, fleets):
        self.create_adjusted_missile(1, to_position, from_position, fleets)

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
