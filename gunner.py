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

    def fire(self, delta_time, missile_tally, saucer_position, saucer_velocity, ship_or_none: Ship | None, fleets):
        if ship_or_none:
            ship_position = ship_or_none.position
        else:
            ship_position = self.random_position()
        self._timer.tick(delta_time, self.fire_missile, missile_tally, saucer_position, saucer_velocity, ship_position, fleets)

    def random_position(self):
        return Vector2(self.random_coordinate(), self.random_coordinate())

    @staticmethod
    def random_coordinate():
        return random.randrange(0, u.SCREEN_SIZE)

    def fire_missile(self, missile_tally, saucer_position, saucer_velocity, ship_position, fleets):
        if missile_tally >= u.SAUCER_MISSILE_LIMIT:
            return
        should_target = random.random()
        self.select_missile(fleets, saucer_position, saucer_velocity, ship_position, should_target)

    def select_missile(self, fleets, saucer_position, saucer_velocity, ship_position, should_target):
        if ship_position and should_target <= u.SAUCER_TARGETING_FRACTION:
            self.create_targeted_missile(saucer_position, ship_position, fleets)
        else:
            random_angle = random.random()
            self.create_random_missile(random_angle, saucer_position, saucer_velocity, fleets)

    def create_random_missile(self, random_angle, saucer_position, saucer_velocity, fleets):
        missile = self.missile_at_angle(saucer_position, random_angle*360.0, saucer_velocity)
        fleets.add_flyer(missile)

    def create_targeted_missile(self, from_position, to_position, fleets):
        best_aiming_point = self.best_aiming_point(from_position, to_position, u.SCREEN_SIZE)
        angle = self.angle_to_hit(best_aiming_point, from_position)
        missile = self.missile_at_angle(from_position, angle, Vector2(0, 0))
        fleets.add_flyer(missile)

    @staticmethod
    def angle_to_hit(best_aiming_point, saucer_position):
        return Vector2(0, 0).angle_to(best_aiming_point - saucer_position)

    def missile_at_angle(self, position, desired_angle, velocity_adjustment):
        missile_velocity = Vector2(u.MISSILE_SPEED, 0).rotate(desired_angle) + velocity_adjustment
        offset = Vector2(2 * self._radius, 0).rotate(desired_angle)
        return Missile.from_saucer(position + offset, missile_velocity)

    def best_aiming_point(self, shooter_position, target_position, wrap_size):
        nearest_x = self.nearest(shooter_position.x, target_position.x, wrap_size)
        nearest_y = self.nearest(shooter_position.y, target_position.y, wrap_size)
        return Vector2(nearest_x, nearest_y)

    @staticmethod
    def nearest(shooter_coord, target_coord, screen_size):
        """ handy diagram      """
        """______|______|______"""
        """ T      T---S++T    """
        """ central T too far away"""
        """ shoot toward right!"""
        direct_distance = abs(target_coord - shooter_coord)
        if direct_distance <= screen_size / 2:
            return target_coord
        elif shooter_coord > target_coord:
            return target_coord + screen_size
        else:
            return target_coord - screen_size
