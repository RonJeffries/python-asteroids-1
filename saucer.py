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
        self._location = MovableLocation(position, velocity)
        self._directions = (velocity.rotate(45), velocity, velocity, velocity.rotate(-45))
        self._missile_tally = 0
        self.create_surface_class_members()
        self.set_firing_timer()
        self.set_zig_timer()

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
        self._missile_tally = 0

    def create_surface_class_members(self):
        if not Saucer.saucer_surface:
            raw_dimensions = Vector2(10, 6)
            saucer_scale = 4 * self.size
            Saucer.offset = raw_dimensions * saucer_scale / 2
            saucer_size = raw_dimensions * saucer_scale
            Saucer.saucer_surface = SurfaceMaker.saucer_surface(saucer_size)

    # noinspection PyAttributeOutsideInit
    def set_firing_timer(self):
        self.missile_timer = Timer(u.SAUCER_MISSILE_DELAY, self.fire_if_missile_available)

    def set_zig_timer(self):
        # noinspection PyAttributeOutsideInit
        self.zig_timer = Timer(u.SAUCER_ZIG_TIME, self.zig_zag_action)

    def zig_zag_action(self):
        self.accelerate_to(self.new_direction())

    def interact_with(self, attacker, fleets):
        attacker.interact_with_saucer(self, fleets)

    def explode(self, fleets):
        player.play("bang_large", self._location)
        player.play("bang_small", self._location)
        fleets.remove_saucer(self)

    def interact_with_asteroid(self, asteroid, fleets):
        if asteroid.are_we_colliding(self.position, self.radius):
            self.explode(fleets)

    def interact_with_missile(self, missile, fleets):
        if missile.is_saucer_missile:
            self._missile_tally += 1
        if missile.are_we_colliding(self.position, self.radius):
            fleets.add_score(Score(self.score_for_hitting(missile)))
            self.explode(fleets)

    def interact_with_ship(self, ship, fleets):
        if ship.are_we_colliding(self.position, self.radius):
            self.explode(fleets)

    def are_we_colliding(self, position, radius):
        kill_range = self.radius + radius
        dist = self.position.distance_to(position)
        return dist <= kill_range

    def draw(self, screen):
        top_left_corner = self.position - Saucer.offset
        screen.blit(Saucer.saucer_surface, top_left_corner)

    def move(self, delta_time, saucers):
        off_x, off_y = self._location.move(delta_time)
        if off_x:
            if self in saucers:
                saucers.remove(self)

    def move_to(self, vector):
        self._location.move_to(vector)

    def check_zigzag(self, delta_time):
        self.zig_timer.tick(delta_time)

    def new_direction(self):
        return random.choice(self._directions)

    def fire_if_possible(self, delta_time, saucer_missiles, ships):
        self.missile_timer.tick(delta_time, saucer_missiles, ships)

    def fire_if_missile_available(self, saucer_missiles, ships) -> bool:
        return saucer_missiles.fire(self.create_missile, ships)

    @staticmethod
    def scores_for_hitting_asteroid():
        return [0, 0, 0]

    @staticmethod
    def scores_for_hitting_saucer():
        return [0, 0]

    def create_missile(self, ships):
        """callback method, called from saucer_missiles.fire"""
        should_target = random.random()
        random_angle = random.random()
        return self.suitable_missile(should_target, random_angle, ships)

    def suitable_missile(self, should_target, random_angle, ships):
        if self.cannot_target_ship(ships, should_target):
            return self.missile_at_angle(random_angle * 360.0, self.velocity_testing_only)
        targeting_angle = self.angle_to(ships[0])
        velocity_adjustment = Vector2(0, 0)
        return self.missile_at_angle(targeting_angle, velocity_adjustment)

    @staticmethod
    def cannot_target_ship(ships, should_target):
        return not ships or should_target > u.SAUCER_TARGETING_FRACTION

    def missile_at_angle(self, desired_angle, velocity_adjustment):
        missile_velocity = Vector2(u.MISSILE_SPEED, 0).rotate(desired_angle) + velocity_adjustment
        offset = Vector2(2 * self.radius, 0).rotate(desired_angle)
        return Missile.from_saucer(self.position + offset, missile_velocity)

    def angle_to(self, ship):
        aiming_point = nearest_point(self.position, ship.position, u.SCREEN_SIZE)
        angle_point = aiming_point - self.position
        return degrees(atan2(angle_point.y, angle_point.x))

    def ready(self):
        pass

    def score_for_hitting(self, attacker):
        return attacker.scores_for_hitting_saucer()[self.size - 1]

    def tick(self, delta_time, fleet, fleets):
        player.play("saucer_big", self._location, False)
        saucer_missiles = fleets.saucer_missiles
        ships = fleets.ships
        self.fire_if_possible(delta_time, saucer_missiles, ships)
        self.check_zigzag(delta_time)
        self.move(delta_time, fleet)


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
