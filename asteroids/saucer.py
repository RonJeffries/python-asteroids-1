# Saucer

from asteroids.explosion import Explosion
from flyer import AsteroidFlyer
from asteroids.gunner import Gunner
from asteroids.movable_location import MovableLocation
from asteroids.painter import Painter
from pygame import Vector2
from asteroids.score import Score
from sounds import player
from core.timer import Timer
import random
import u


class Saucer(AsteroidFlyer):
    direction = -1
    saucer_surface = None
    offset = None

    @classmethod
    def init_for_new_game(cls):
        cls.direction = -1

    @classmethod
    def small(cls):
        return cls(radius=10, score=1000, sound="saucer_small", is_small=True, always_target=True, scale=4)

    @classmethod
    def large(cls):
        return cls(radius=20, score=200, sound="saucer_big", is_small=False, always_target=False, scale=8)

    def __init__(self, radius, score, sound, is_small, always_target, scale):
        Saucer.direction = -Saucer.direction
        x = 0 if Saucer.direction > 0 else u.SCREEN_SIZE
        position = Vector2(x, random.randrange(0, u.SCREEN_SIZE))
        velocity = Saucer.direction * u.SAUCER_VELOCITY
        self._directions = (velocity.rotate(45), velocity, velocity, velocity.rotate(-45))
        self._gunner = Gunner(always_target)
        self._location = MovableLocation(position, velocity)
        self._radius = radius * u.SCALE_FACTOR
        self._painter = Painter.saucer(scale * u.SCALE_FACTOR)
        self._score = score
        self._ship_to_target = None
        self._sound = sound
        self._zig_timer = Timer(u.SAUCER_ZIG_TIME)
        self.is_small_saucer = is_small
        self.missile_tally = 0
        self.missile_head_start = 2*self._radius

    @property
    def position(self):
        return self._location.position

    @property
    def velocity(self):
        return self._location.velocity

    def accelerate_to(self, velocity):
        self._location.accelerate_to(velocity)

    def begin_interactions(self, fleets):
        self._ship_to_target = None
        self.missile_tally = 0

    def interact_with(self, attacker, fleets):
        attacker.interact_with_saucer(self, fleets)

    def interact_with_asteroid(self, asteroid, fleets):
        if asteroid.are_we_colliding(self.position, self._radius):
            self.explode(fleets)

    def interact_with_missile(self, missile, fleets):
        missile.ping_transponder("saucer", self.increment_tally)
        if missile.are_we_colliding(self.position, self._radius):
            missile.ping_transponder("ship", self.score_points, fleets)
            self.explode(fleets)

    def score_points(self, fleets):
        fleets.append(Score(self._score))

    def increment_tally(self):
        self.missile_tally += 1

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        self._ship_to_target = ship
        if ship.are_we_colliding(self.position, self._radius):
            self.explode(fleets)

    def are_we_colliding(self, position, radius):
        kill_range = self._radius + radius
        dist = self.position.distance_to(position)
        return dist <= kill_range

    def draw(self, screen):
        self._painter.draw(screen, self.position)

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
        self._gunner.fire(delta_time, self, self._ship_to_target, fleets)

    def tick(self, delta_time, fleets):
        pass

    def update(self, delta_time, fleets):
        player.play(self._sound, self._location, False)
        self.fire_if_possible(delta_time, fleets)
        self.check_zigzag(delta_time)
        self._move(delta_time, fleets)

    def zig_zag_action(self):
        self.accelerate_to(self.new_direction())

