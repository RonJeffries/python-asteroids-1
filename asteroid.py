# Asteroid

import pygame
from pygame.math import Vector2
import random
from SurfaceMaker import SurfaceMaker
import u


class Asteroid:
    def __init__(self, size=2, position=None):
        self.position = position if position else Vector2(0, random.randrange(0, u.SCREEN_SIZE))
        angle_of_travel = random.randint(0, 360)
        self.velocity = u.ASTEROID_SPEED.rotate(angle_of_travel)
        asteroid_radii = [16, 32, 64]
        try:
            self.radius = asteroid_radii[size]
        except IndexError:
            self.radius = asteroid_radii[2]
        self.offset = Vector2(self.radius, self.radius)
        self.surface = SurfaceMaker.asteroid_surface(self.radius * 2)

    def draw(self, screen):
        top_left_corner = self.position - self.offset
        pygame.draw.circle(screen, "red", self.position, 3)
        screen.blit(self.surface, top_left_corner)

    def move(self, deltaTime):
        position = self.position + self.velocity * deltaTime
        position.x = position.x % u.SCREEN_SIZE
        position.y = position.y % u.SCREEN_SIZE
        self.position = position

    def withinRange(self, point, other_radius):
        dist = point.distance_to(self.position)
        return dist < self.radius + other_radius
