# Saucer

import random
from math import atan2, degrees

from pygame import Vector2
import u
from SurfaceMaker import SurfaceMaker
from missile import Missile


class Saucer:
    def __init__(self, position=None, size=2):
        self.position = position if position is not None else u.CENTER
        self.size = size
        self.velocity = u.SAUCER_VELOCITY
        self.directions = (self.velocity.rotate(45), self.velocity, self.velocity, self.velocity.rotate(-45))
        self.direction = -1
        self.radius = 20
        raw_dimensions = Vector2(10, 6)
        saucer_scale = 4 * self.size
        self.offset = raw_dimensions * saucer_scale / 2
        saucer_size = raw_dimensions * saucer_scale
        self.saucer_surface = SurfaceMaker.saucer_surface(saucer_size)
        self.zig_timer = 1.5
        self.missile_timer = u.SAUCER_MISSILE_DELAY

    def destroyed_by(self, attacker, saucers):
        if self in saucers: saucers.remove(self)

    def draw(self, screen):
        top_left_corner = self.position - self.offset
        screen.blit(self.saucer_surface, top_left_corner)

    def init_for_new_game(self):
        self.direction = -1

    def move(self, delta_time, saucers, saucer_missiles, ships):
        self.fire_if_possible(delta_time, saucer_missiles, ships)
        self.check_zigzag(delta_time)
        self.position += delta_time * self.velocity
        x = self.position.x
        if x < 0 or x > u.SCREEN_SIZE:
            if self in saucers:
                saucers.remove(self)

    def check_zigzag(self, delta_time):
        self.zig_timer -= delta_time
        if self.zig_timer <= 0:
            self.zig_timer = u.SAUCER_ZIG_TIME
            self.velocity = self.new_direction() * self.direction

    def new_direction(self):
        return random.choice(self.directions)

    def fire_if_possible(self, delta_time, saucer_missiles, ships):
        if self.firing_is_possible(delta_time, saucer_missiles):
            self.fire_a_missile(saucer_missiles, ships)

    def fire_a_missile(self, saucer_missiles, ships):
        saucer_missiles.append(self.create_missile(ships))
        self.missile_timer = u.SAUCER_MISSILE_DELAY

    def firing_is_possible(self, delta_time, saucer_missiles):
        return self.missile_timer_expired(delta_time) and self.a_missile_is_available(saucer_missiles)

    def scores_for_hitting_asteroid(self):
        return [0, 0, 0]

    def scores_for_hitting_saucer(self):
        return [0, 0]

    def missile_at_angle(self, degrees, velocity_adjustment):
        missile_velocity = Vector2(u.MISSILE_SPEED, 0).rotate(degrees) + velocity_adjustment
        offset = Vector2(2 * self.radius, 0).rotate(degrees)
        return Missile.from_saucer(self.position + offset, missile_velocity)

    def missile_timer_expired(self, delta_time):
        self.missile_timer -= delta_time
        expired = self.missile_timer <= 0
        return expired

    @staticmethod
    def a_missile_is_available(saucer_missiles):
        return len(saucer_missiles) < u.SAUCER_MISSILE_LIMIT

    def create_missile(self, ships):
        should_target = random.random()
        random_angle = random.random()
        return self.suitable_missile(should_target, random_angle, ships)

    def suitable_missile(self, should_target, random_angle, ships):
        if self.targeting_ship(ships, should_target):
            targeting_angle = self.angle_to(ships[0])
            zero_velocity = Vector2(0, 0)
            return self.missile_at_angle(targeting_angle, zero_velocity)
        return self.missile_at_angle(random_angle * 360.0, self.velocity)

    def targeting_ship(self, ships, should_target):
        return ships and should_target <= u.SAUCER_TARGETING_FRACTION

    def angle_to(self, ship):
        aiming_point = nearest_point(self.position, ship.position, u.SCREEN_SIZE)
        angle_point = aiming_point - self.position
        return degrees(atan2(angle_point.y, angle_point.x))

    def ready(self):
        self.direction = -self.direction
        self.velocity = self.direction * u.SAUCER_VELOCITY
        x = 0 if self.direction > 0 else u.SCREEN_SIZE
        self.position = Vector2(x, random.randrange(0, u.SCREEN_SIZE))
        self.missile_timer = u.SAUCER_MISSILE_DELAY
        self.zig_timer = u.SAUCER_ZIG_TIME

    def score_for_hitting(self, attacker):
        return attacker.scores_for_hitting_saucer()[self.size - 1]


def nearest(shooter, target, size):
    dist = abs(target - shooter)
    t_min = target - size
    t_min_dist = abs(t_min - shooter)
    t_max = target + size
    t_max_dist = abs(t_max - shooter)
    if t_min_dist < dist:
        return t_min
    elif t_max_dist < dist:
        return t_max
    else:
        return target


def nearest_point(shooter, target, size):
    nearest_x = nearest(shooter.x, target.x, size)
    nearest_y = nearest(shooter.y, target.y, size)
    return Vector2(nearest_x, nearest_y)
