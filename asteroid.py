# Asteroid

import pygame
from pygame.math import Vector2
import random
from SurfaceMaker import SurfaceMaker
import u


class Asteroid:
    def __init__(self, size=2, position=None):
        self.mover = self
        asteroid_sizes = [32, 64, 128]
        try:
            asteroid_size = asteroid_sizes[size]
        except IndexError:
            asteroid_size = asteroid_sizes[2]
        self.offset = Vector2(asteroid_size/2, asteroid_size/2)
        self.position = position if position else Vector2(0, random.randrange(0, u.SCREEN_SIZE))
        angle_of_travel = random.randint(0, 360)
        self.velocity = u.ASTEROID_SPEED.rotate(angle_of_travel)
        self.surface = SurfaceMaker.asteroid_surface(asteroid_size)

    def draw(self, screen):
        top_left_corner = self.position - self.offset
        pygame.draw.circle(screen, "red", self.position, 3)
        screen.blit(self.surface, top_left_corner)

    def move(self, dt):
        self.position += self.velocity * dt
        self.position.x = self.position.x % u.SCREEN_SIZE
        self.position.y = self.position.y % u.SCREEN_SIZE
