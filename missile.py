# Missile

import pygame
import u
from timer import Timer


class Missile:
    def __init__(self, position, velocity, missile_score_list, saucer_score_list):
        self.score_list = missile_score_list
        self.saucer_score_list = saucer_score_list
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.radius = 2
        self.timer = Timer(u.MISSILE_LIFETIME, self.timeout)

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

    def destroyed_by(self, attacker, missiles):
        if self in missiles: missiles.remove(self)

    def score_for_hitting(self, _anyone):
        return 0

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, 4)

    def move(self, deltaTime, _missiles):
        position = self.position + self.velocity * deltaTime
        position.x = position.x % u.SCREEN_SIZE
        position.y = position.y % u.SCREEN_SIZE
        self.position = position

    def update(self, missiles, delta_time):
        self.timer.tick(delta_time, missiles)

    def timeout(self, missiles):
        missiles.remove(self)

