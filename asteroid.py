import random

import pygame
from pygame.math import clamp, Vector2

import u
from SurfaceMaker import SurfaceMaker


class Asteroid:
    def __init__(self, size=2, position=None):
        self.position = position if position else Vector2(0, random.randrange(0, u.SCREEN_SIZE))
        offset_amount = [16, 32, 64][clamp(size, 0, 2)]
        self.offset = Vector2(offset_amount, offset_amount)
        print(self.offset)
        angle_of_travel = random.randint(0, 360)
        self.velocity = u.ASTEROID_SPEED.rotate(angle_of_travel)
        self.surface = SurfaceMaker.asteroid_surface(size)

    def move(self, dt):
        self.position += self.velocity * dt
        self.position.x = self.position.x % u.SCREEN_SIZE
        self.position.y = self.position.y % u.SCREEN_SIZE

    def draw(self, screen):
        top_left_corner = self.position - self.offset
        pygame.draw.circle(screen, "red", self.position, 3)
        screen.blit(self.surface, top_left_corner)
