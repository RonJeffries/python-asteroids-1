import random

from pygame import Vector2

import u
from missile import Missile
from timer import Timer


class Gunner:
    def __init__(self, saucer_radius=20):
        self._timer = Timer(u.SAUCER_MISSILE_DELAY)
        self._radius = saucer_radius

    def fire(self, delta_time, missile_tally, saucer_position, saucer_velocity, ship_position, fleets):
        self._timer.tick(delta_time, self.fire_missile, missile_tally, saucer_position, saucer_velocity, ship_position, fleets)

    def fire_missile(self, missile_tally, saucer_position, saucer_velocity, ship_position, fleets):
        if missile_tally >= u.SAUCER_MISSILE_LIMIT:
            return
        should_target = random.random()
        random_angle = random.random()
        self.create_missile(should_target, random_angle, saucer_position, saucer_velocity, ship_position, fleets)

    def create_missile(self, should_target, random_angle, saucer_position, saucer_velocity, ship_position, fleets):
        if ship_position and should_target <= u.SAUCER_TARGETING_FRACTION:
            self.create_targeted_missile(saucer_position, ship_position, fleets)
        else:
            self.create_random_missile(random_angle, saucer_position, saucer_velocity, fleets)

    def create_random_missile(self, random_angle, saucer_position, saucer_velocity, fleets):
        missile = self.missile_at_angle(saucer_position, random_angle*360.0, saucer_velocity)
        fleets.add_flyer(missile)

    def missile_at_angle(self, position, desired_angle, velocity_adjustment):
        missile_velocity = Vector2(u.MISSILE_SPEED, 0).rotate(desired_angle) + velocity_adjustment
        offset = Vector2(2 * self._radius, 0).rotate(desired_angle)
        return Missile.from_saucer(position + offset, missile_velocity)

    def create_targeted_missile(self, saucer_position, ship_position, fleets):
        aiming_point = nearest_point(saucer_position, ship_position, u.SCREEN_SIZE)
        angle = Vector2(0, 0).angle_to(aiming_point - saucer_position)
        missile = self.missile_at_angle(saucer_position, angle, Vector2(0, 0))
        fleets.add_flyer(missile)


def nearest_point(shooter, target, wrap_size):
    nearest_x = nearest(shooter.x, target.x, wrap_size)
    nearest_y = nearest(shooter.y, target.y, wrap_size)
    return Vector2(nearest_x, nearest_y)


def nearest(shooter, target, wrap_size):
    direct_distance = abs(target - shooter)
    target_wrap_left = target - wrap_size
    wrap_left_distance = abs(target_wrap_left - shooter)
    target_wrap_right = target + wrap_size
    wrap_right_distance = abs(target_wrap_right - shooter)
    if wrap_left_distance < direct_distance:
        return target_wrap_left
    elif wrap_right_distance < direct_distance:
        return target_wrap_right
    else:
        return target
