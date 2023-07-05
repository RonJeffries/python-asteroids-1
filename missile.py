
# Missile
from flyer import Flyer
from movable_location import MovableLocation
from timer import Timer
from transponder import Transponder
from typing import Callable
import pygame
import u


class Missile(Flyer):
    confirm_score: Callable[[int], int]

    Saucer = None
    radius = 2

    @classmethod
    def from_saucer(cls, transponder_key, position, velocity):
        return cls(transponder_key, position, velocity, [0, 0, 0], lambda score: 0, False)

    @classmethod
    def from_ship(cls, transponder_key, position, velocity):
        return cls(transponder_key, position, velocity, u.ASTEROID_SCORE_LIST, lambda score: score, True)

    def __init__(self, transponder_key, position, velocity, missile_score_list, confirmation, from_ship):
        self._transponder = Transponder(transponder_key)
        self.confirm_score = confirmation
        self.score_list = missile_score_list
        self._timer = Timer(u.MISSILE_LIFETIME)
        self._location = MovableLocation(position, velocity)

    @property
    def position(self):
        return self._location.position

    @property
    def velocity_testing_only(self):
        return self._location.velocity

    def are_we_colliding(self, position, radius):
        kill_range = self.radius + radius
        dist = self.position.distance_to(position)
        return dist <= kill_range

    def interact_with(self, attacker, fleets):
        attacker.interact_with_missile(self, fleets)

    def interact_with_asteroid(self, asteroid, fleets):
        if asteroid.are_we_colliding(self.position, self.radius):
            self.die(fleets)

    def interact_with_missile(self, missile, fleets):
        if missile.are_we_colliding(self.position, self.radius):
            self.die(fleets)

    def interact_with_saucer(self, saucer, fleets):
        if saucer.are_we_colliding(self.position, self.radius):
            self.die(fleets)

    def interact_with_ship(self, ship, fleets):
        if ship.are_we_colliding(self.position, self.radius):
            self.die(fleets)

    def die(self, fleets):
        fleets.remove(self)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, 4)

    def ping_transponder(self, transponder_key, function):
        self._transponder.ping(transponder_key, function)

    def tick(self, delta_time, fleets):
        self.tick_timer(delta_time, fleets)

    def tick_timer(self, delta_time, fleets):
        self._timer.tick(delta_time, self.die, fleets)

    def update(self, delta_time, _fleets):
        self._location.move(delta_time)

