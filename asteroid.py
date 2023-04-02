# Asteroid

import pygame
from pygame.math import Vector2
import random
from SurfaceMaker import SurfaceMaker
import u
from mover import Mover


class Asteroid:
    def __init__(self, size=2, position=None):
        asteroid_sizes = [32, 64, 128]
        try:
            asteroid_size = asteroid_sizes[size]
        except IndexError:
            asteroid_size = asteroid_sizes[2]
        self.offset = Vector2(asteroid_size/2, asteroid_size/2)
        mover_position = position if position else Vector2(0, random.randrange(0, u.SCREEN_SIZE))
        angle_of_travel = random.randint(0, 360)
        mover_velocity = velocity = u.ASTEROID_SPEED.rotate(angle_of_travel)
        self.mover = Mover(mover_position, mover_velocity)
        self.surface = SurfaceMaker.asteroid_surface(asteroid_size)

    def draw(self, screen):
        top_left_corner = self.mover.position - self.offset
        pygame.draw.circle(screen, "red", self.mover.position, 3)
        screen.blit(self.surface, top_left_corner)
