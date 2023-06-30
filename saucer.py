# Saucer

import random
from math import atan2, degrees

from pygame import Vector2
import u
from SurfaceMaker import SurfaceMaker
from explosion import Explosion
from flyer import Flyer
from gunner import Gunner
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

    def __init__(self, size=2):
        Saucer.direction = -Saucer.direction
        x = 0 if Saucer.direction > 0 else u.SCREEN_SIZE
        position = Vector2(x, random.randrange(0, u.SCREEN_SIZE))
        velocity = Saucer.direction * u.SAUCER_VELOCITY
        self._directions = (velocity.rotate(45), velocity, velocity, velocity.rotate(-45))
        self._gunner = Gunner()
        self._location = MovableLocation(position, velocity)
        self._radius = 10*size  # getting ready for small saucer
        self._ship = None
        self._size = size
        self._zig_timer = Timer(u.SAUCER_ZIG_TIME)
        self.missile_tally = 0
        self.missile_head_start = 2*self._radius
        self.create_surface_class_members()

    @property
    def position(self):
        return self._location.position

    @property
    def velocity(self):
        return self._location.velocity

    @property
    def always_target(self):
        return self._size == 1

    def accelerate_to(self, velocity):
        self._location.accelerate_to(velocity)

    def begin_interactions(self, fleets):
        self._ship = None
        self.missile_tally = 0

    def create_surface_class_members(self):
        raw_dimensions = Vector2(10, 6)
        saucer_scale = 4 * self._size
        Saucer.offset = raw_dimensions * saucer_scale / 2
        saucer_size = raw_dimensions * saucer_scale
        Saucer.saucer_surface = SurfaceMaker.saucer_surface(saucer_size)

    def interact_with(self, attacker, fleets):
        attacker.interact_with_saucer(self, fleets)

    def interact_with_asteroid(self, asteroid, fleets):
        if asteroid.are_we_colliding(self.position, self._radius):
            self.explode(fleets)

    def interact_with_fragment(self, fragment, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        self.missile_tally += missile.saucer_tally
        if missile.are_we_colliding(self.position, self._radius):
            fleets.append(Score(self.score_for_hitting(missile)))
            self.explode(fleets)

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        self._ship = ship
        if ship.are_we_colliding(self.position, self._radius):
            self.explode(fleets)

    def are_we_colliding(self, position, radius):
        kill_range = self._radius + radius
        dist = self.position.distance_to(position)
        return dist <= kill_range

    def draw(self, screen):
        top_left_corner = self.position - Saucer.offset
        screen.blit(Saucer.saucer_surface, top_left_corner)

    def explode(self, fleets):
        player.play("bang_large", self._location)
        player.play("bang_small", self._location)
        fleets.remove(self)
        Explosion.from_saucer(self.position, fleets)

    def _move(self, delta_time, fleets):
        off_x, off_y = self._location.move(delta_time)
        if off_x:
            fleets.remove(self)

    def move_to(self, vector):
        self._location.move_to(vector)

    def check_zigzag(self, delta_time):
        self._zig_timer.tick(delta_time, self.zig_zag_action)

    def new_direction(self):
        return random.choice(self._directions)

    def fire_if_possible(self, delta_time, fleets):
        self._gunner.fire(delta_time, self, self._ship, fleets)

    @staticmethod
    def scores_for_hitting_asteroid():
        return [0, 0, 0]

    @staticmethod
    def scores_for_hitting_saucer():
        return [0, 0]

    def score_for_hitting(self, attacker):
        return attacker.scores_for_hitting_saucer()[self._size - 1]

    def tick(self, delta_time, fleets):
        pass

    def update(self, delta_time, fleets):
        if self._ship == 2:
            player.play("saucer_big", self._location, False)
        else:
            player.play("saucer_small", self._location, False)
        self.fire_if_possible(delta_time, fleets)
        self.check_zigzag(delta_time)
        self._move(delta_time, fleets)

    def zig_zag_action(self):
        self.accelerate_to(self.new_direction())