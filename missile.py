# Missile

import pygame
from mover import Mover


class Missile:
    def __init__(self, position, velocity):
        self.radius = 2
        self.mover = Mover(position, velocity)
        self.time = 0

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.mover.position, 4)

    def update(self, missiles, delta_time):
        self.time += delta_time
        if self.time > 3:
            missiles.remove(self)

