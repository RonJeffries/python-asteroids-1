# Missile

import pygame
import u
from movable_location import MovableLocation
from timer import Timer


class Missile:
    def __init__(self, position, velocity, missile_score_list, saucer_score_list):
        self.score_list = missile_score_list
        self.saucer_score_list = saucer_score_list
        self.location = MovableLocation(position, velocity)
        self.radius = 2
        self.timer = Timer(u.MISSILE_LIFETIME, self.timeout)

    @property
    def position(self):
        return self.location.position

    @property
    def velocity(self):
        return self.location.velocity

    @classmethod
    def from_ship(cls, position, velocity):
        return cls(position, velocity, u.MISSILE_SCORE_LIST, u.SAUCER_SCORE_LIST)

    @classmethod
    def from_saucer(cls, position, velocity):
        return cls(position, velocity, [0, 0, 0], [0, 0])

    def scores_for_hitting_asteroid(self):
        return self.score_list

    def scores_for_hitting_saucer(self):
        return self.saucer_score_list

    def destroyed_by(self, _attacker, missiles, _fleets):
        if self in missiles:
            missiles.remove(self)

    @staticmethod
    def score_for_hitting(_anyone):
        return 0

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, 4)

    def move(self, delta_time):
        self.location.move(delta_time)

    def tick_timer(self, delta_time, missiles):
        self.timer.tick(delta_time, missiles)

    def tick(self, delta_time, fleet, _fleets):
        # see if I can push
        self.tick_timer(delta_time, fleet)
        self.move(delta_time)
        return True

    def timeout(self, missiles):
        missiles.remove(self)
