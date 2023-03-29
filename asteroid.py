import random

import pygame
import u
from SurfaceMaker import SurfaceMaker

vector2 = pygame.Vector2


class Asteroid:
    def __init__(self):
        self.position = vector2(u.SCREEN_SIZE/2, u.SCREEN_SIZE/2)
        angle_of_travel = random.randint(0, 360)
        self.velocity = u.ASTEROID_SPEED.rotate(angle_of_travel)
        self.surface = SurfaceMaker().asteroid_surface(shape=0, size=3)

    def move(self, dt):
        self.position += self.velocity*dt
        self.position.x = self.position.x % u.SCREEN_SIZE
        self.position.y = self.position.y % u.SCREEN_SIZE

    def draw(self, screen):
        half = vector2(self.surface.get_size()) / 2
        screen.blit(self.surface, self.position - half)
