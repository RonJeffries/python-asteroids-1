# Missile

import pygame
import u
from movable_location import MovableLocation
from timer import Timer


class Missile:
    Saucer = None

    def __init__(self, position, velocity, missile_score_list, saucer_score_list):
        self.score_list = missile_score_list
        self.radius = 2
        self._timer = Timer(u.MISSILE_LIFETIME, self.timeout)
        self._saucer_score_list = saucer_score_list
        self._location = MovableLocation(position, velocity)

    @property
    def position(self):
        return self._location.position

    @property
    def velocity_testing_only(self):
        return self._location.velocity

    @classmethod
    def from_ship(cls, position, velocity):
        return cls(position, velocity, u.MISSILE_SCORE_LIST, u.SAUCER_SCORE_LIST)

    @classmethod
    def from_saucer(cls, position, velocity):
        return cls(position, velocity, [0, 0, 0], [0, 0])

    def are_we_colliding(self, position, radius):
        kill_range = self.radius + radius
        dist = self.position.distance_to(position)
        return dist <= kill_range

    def scores_for_hitting_asteroid(self):
        return self.score_list

    def scores_for_hitting_saucer(self):
        return self._saucer_score_list

    def interact_with(self, attacker, fleets):
        attacker.interact_with_missile(self, fleets)

    def interact_with_asteroid(self, asteroid, fleets):
        if asteroid.are_we_colliding(self.position, self.radius):
            self.die(fleets)

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        if saucer.are_we_colliding(self.position, self.radius):
            self.die(fleets)

    def interact_with_score(self, score, fleets):
        pass

    def interact_with_scorekeeper(self, scorekeeper, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        if ship.are_we_colliding(self.position, self.radius):
            self.die(fleets)

    def die(self, fleets):
        fleets.remove_missile(self)

    @staticmethod
    def score_for_hitting(_anyone):
        return 0

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, 4)

    def move(self, delta_time):
        self._location.move(delta_time)

    def tick_timer(self, delta_time, missiles):
        self._timer.tick(delta_time, missiles)

    def tick(self, delta_time, fleet, _fleets):
        self.tick_timer(delta_time, fleet)
        self.move(delta_time)

    def timeout(self, missiles):
        missiles.remove(self)
