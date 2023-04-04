# Asteroid

import pygame
from pygame.math import Vector2
import random
from SurfaceMaker import SurfaceMaker
import u


class Asteroid:
    def __init__(self, size=2, position=None):
        self.size = size
        if self.size not in [0,1,2]:
            self.size = 2
        self.radius = [16, 32, 64][self.size]
        self.position = position if position else Vector2(0, random.randrange(0, u.SCREEN_SIZE))
        angle_of_travel = random.randint(0, 360)
        self.velocity = u.ASTEROID_SPEED.rotate(angle_of_travel)
        self.offset = Vector2(self.radius, self.radius)
        self.surface = SurfaceMaker.asteroid_surface(self.radius * 2)

    def draw(self, screen):
        top_left_corner = self.position - self.offset
        pygame.draw.circle(screen, "red", self.position, 3)
        screen.blit(self.surface, top_left_corner)

    def move(self, delta_time):
        position = self.position + self.velocity * delta_time
        position.x = position.x % u.SCREEN_SIZE
        position.y = position.y % u.SCREEN_SIZE
        self.position = position

    def withinRange(self, point, other_radius):
        dist = point.distance_to(self.position)
        return dist < self.radius + other_radius

    def collide_with_missile(self, missile, missiles, asteroids):
        if self.withinRange(missile.position, missile.radius):
            missiles.remove(missile)
            self.split_or_die(asteroids)

    def split_or_die(self, asteroids):
        asteroids.remove(self)
        size = [16, 32, 64].index(self.radius)
        if size > 0:
            a1 = Asteroid(size - 1, self.position)
            asteroids.append(a1)
            a2 = Asteroid(size - 1, self.position)
            asteroids.append(a2)
