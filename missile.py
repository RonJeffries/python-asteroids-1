# Missile

import pygame

import u
from mover import Mover


class Missile:
    def __init__(self, position, velocity):
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.radius = 2
        self.mover = self
        self.time = 0

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.mover.position, 4)

    def move(self, deltaTime):
        position = self.position + self.velocity * deltaTime
        position.x = position.x % u.SCREEN_SIZE
        position.y = position.y % u.SCREEN_SIZE
        self.position = position

    def update(self, missiles, delta_time):
        self.time += delta_time
        if self.time > 3:
            missiles.remove(self)

