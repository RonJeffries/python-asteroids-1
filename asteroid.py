# Asteroid

import pygame
from pygame.math import Vector2
import random
from SurfaceMaker import SurfaceMaker
import u
from mover import Mover


class Asteroid:
    def __init__(self, size=2, position=None):
        asteroid_radii = [16, 32, 64]
        try:
            self.radius = asteroid_radii[size]
        except IndexError:
            self.radius = asteroid_radii[2]
        self.offset = Vector2(self.radius, self.radius)
        mover_position = position if position else Vector2(0, random.randrange(0, u.SCREEN_SIZE))
        angle_of_travel = random.randint(0, 360)
        mover_velocity = u.ASTEROID_SPEED.rotate(angle_of_travel)
        self.mover = Mover(mover_position, mover_velocity)
        self.surface = SurfaceMaker.asteroid_surface(self.radius * 2)

    def draw(self, screen):
        top_left_corner = self.mover.position - self.offset
        pygame.draw.circle(screen, "red", self.mover.position, 3)
        screen.blit(self.surface, top_left_corner)

    def withinRange(self, point, other_radius):
        dist = point.distance_to(self.mover.position)
        return dist < self.radius + other_radius
