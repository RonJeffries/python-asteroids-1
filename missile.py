# Missile

import pygame
import u


class Missile:
    def __init__(self, position, velocity, missile_score_list, saucer_score_list):
        self.score_list = missile_score_list
        self.saucer_score_list = saucer_score_list
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.radius = 2
        self.time = 0

    @classmethod
    def from_ship(cls, position, velocity):
        return cls(position, velocity, u.MISSILE_SCORE_LIST, u.SAUCER_SCORE_LIST)

    @classmethod
    def from_saucer(cls, position, velocity):
        return cls(position, velocity, [0, 0, 0], [0, 0])

    def get_asteroid_scores(self):
        return self.score_list

    def get_saucer_scores(self):
        return self.saucer_score_list

    def destroyed_by(self, attacker, missiles):
        if self in missiles: missiles.remove(self)

    def score_for_hitting(self, _anyone):
        return 0

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, 4)

    def move(self, deltaTime):
        position = self.position + self.velocity * deltaTime
        position.x = position.x % u.SCREEN_SIZE
        position.y = position.y % u.SCREEN_SIZE
        self.position = position

    def update(self, missiles, delta_time):
        self.time += delta_time
        if self.time > u.MISSILE_LIFETIME:
            missiles.remove(self)

