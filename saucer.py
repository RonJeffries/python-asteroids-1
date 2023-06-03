# Saucer

import random
from math import atan2, degrees

from pygame import Vector2
import u
from SurfaceMaker import SurfaceMaker
from flyer import Flyer
from missile import Missile
from movable_location import MovableLocation
from score import Score
from sounds import player
from timer import Timer


class Saucer(Flyer):
    direction = -1
    saucer_surface = None
    offset = None

    @classmethod
    def init_for_new_game(cls):
        cls.direction = -1

    def __init__(self, _position=None, size=2):
        self.radius = 20
        self.size = size
        Saucer.direction = -Saucer.direction
        x = 0 if Saucer.direction > 0 else u.SCREEN_SIZE
        position = Vector2(x, random.randrange(0, u.SCREEN_SIZE))
        velocity = Saucer.direction * u.SAUCER_VELOCITY
        self._missile_tally = 0
        self._location = MovableLocation(position, velocity)
        self._directions = (velocity.rotate(45), velocity, velocity, velocity.rotate(-45))
        self._create_surface_class_members()
        self._set_firing_timer()
        self._set_zig_timer()
        self.ship = None

    @property
    def position(self):
        return self._location.position

    @property
    def _velocity(self):
        return self._location.velocity

    @property
    def velocity_testing_only(self):
        return self._velocity

    def accelerate_to(self, velocity):
        self._location.accelerate_to(velocity)

    def begin_interactions(self, fleets):
        self.ship = None
        self._missile_tally = 0

    def _create_surface_class_members(self):
        if not Saucer.saucer_surface:
            raw_dimensions = Vector2(10, 6)
            saucer_scale = 4 * self.size
            Saucer.offset = raw_dimensions * saucer_scale / 2
            saucer_size = raw_dimensions * saucer_scale
            Saucer.saucer_surface = SurfaceMaker.saucer_surface(saucer_size)

    def _set_firing_timer(self):
        # noinspection PyAttributeOutsideInit
        self.missile_timer = Timer(u.SAUCER_MISSILE_DELAY)

    def _set_zig_timer(self):
        # noinspection PyAttributeOutsideInit
        self.zig_timer = Timer(u.SAUCER_ZIG_TIME)

    def zig_zag_action(self):
        self.accelerate_to(self.new_direction())

    def interact_with(self, attacker, fleets):
        attacker.interact_with_saucer(self, fleets)

    def explode(self, fleets):
        player.play("bang_large", self._location)
        player.play("bang_small", self._location)
        fleets.remove_flyer(self)

    def interact_with_asteroid(self, asteroid, fleets):
        if asteroid.are_we_colliding(self.position, self.radius):
            self.explode(fleets)

    def interact_with_missile(self, missile, fleets):
        if missile.is_saucer_missile:
            self._missile_tally += 1
        if missile.are_we_colliding(self.position, self.radius):
            fleets.add_flyer(Score(self.score_for_hitting(missile)))
            self.explode(fleets)

    def interact_with_ship(self, ship, fleets):
        self.ship = ship
        if ship.are_we_colliding(self.position, self.radius):
            self.explode(fleets)

    def are_we_colliding(self, position, radius):
        kill_range = self.radius + radius
        dist = self.position.distance_to(position)
        return dist <= kill_range

    def draw(self, screen):
        top_left_corner = self.position - Saucer.offset
        screen.blit(Saucer.saucer_surface, top_left_corner)

    def _move(self, delta_time, fleets):
        off_x, off_y = self._location.move(delta_time)
        if off_x:
            fleets.remove_flyer(self)

    def move_to(self, vector):
        self._location.move_to(vector)

    def check_zigzag(self, delta_time):
        self.zig_timer.tick(delta_time, self.zig_zag_action)

    def new_direction(self):
        return random.choice(self._directions)

    def fire_if_possible(self, delta_time, fleets):
        self.missile_timer.tick(delta_time, self.fire_if_missile_available, fleets)

    def fire_if_missile_available(self, fleets) -> bool:
        if self._missile_tally >= u.SAUCER_MISSILE_LIMIT:
            return False
        missile = self.create_missile()
        fleets.add_flyer(missile)
        return True

    @staticmethod
    def scores_for_hitting_asteroid():
        return [0, 0, 0]

    @staticmethod
    def scores_for_hitting_saucer():
        return [0, 0]

    def create_missile(self):
        """callback method, called from saucer_missiles.fire"""
        should_target = random.random()
        random_angle = random.random()
        return self.suitable_missile(should_target, random_angle)

    def suitable_missile(self, should_target, random_angle):
        if self.cannot_target_ship(should_target):
            return self.missile_at_angle(random_angle * 360.0, self._velocity)
        else:
            targeting_angle = self.angle_to(self.ship)
            velocity_adjustment = Vector2(0, 0)
            return self.missile_at_angle(targeting_angle, velocity_adjustment)

    def cannot_target_ship(self, should_target):
        return not self.ship or should_target > u.SAUCER_TARGETING_FRACTION

    def missile_at_angle(self, desired_angle, velocity_adjustment):
        missile_velocity = Vector2(u.MISSILE_SPEED, 0).rotate(desired_angle) + velocity_adjustment
        offset = Vector2(2 * self.radius, 0).rotate(desired_angle)
        return Missile.from_saucer(self.position + offset, missile_velocity)

    def angle_to(self, ship):
        aiming_point = nearest_point(self.position, ship.position, u.SCREEN_SIZE)
        angle_point = aiming_point - self.position
        return degrees(atan2(angle_point.y, angle_point.x))

    def score_for_hitting(self, attacker):
        return attacker.scores_for_hitting_saucer()[self.size - 1]

    def move(self, delta_time, fleets):
        player.play("saucer_big", self._location, False)
        self.fire_if_possible(delta_time, fleets)
        self.check_zigzag(delta_time)
        self._move(delta_time, fleets)

    def tick(self, delta_time, fleet, fleets):
        pass


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


def nearest_point(shooter, target, wrap_size):
    nearest_x = nearest(shooter.x, target.x, wrap_size)
    nearest_y = nearest(shooter.y, target.y, wrap_size)
    return Vector2(nearest_x, nearest_y)
