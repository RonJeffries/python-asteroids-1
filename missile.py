
# Missile
import pygame

import u
from flyer import Flyer
from movable_location import MovableLocation
from timer import Timer
from transponder import Transponder


class Missile(Flyer):
    Saucer = None
    radius = 2

    def __init__(self, transponder_key, position, velocity):
        self._transponder = Transponder(transponder_key)
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

    def ping_transponder(self, transponder_key, function, *args):
        self._transponder.ping(transponder_key, function, *args)

    def tick(self, delta_time, fleets):
        self.tick_timer(delta_time, fleets)

    def tick_timer(self, delta_time, fleets):
        self._timer.tick(delta_time, self.die, fleets)

    def update(self, delta_time, _fleets):
        self._location.move(delta_time)

