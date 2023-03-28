import random
from itertools import repeat

import pygame
import u
from SurfaceMaker import raw_rocks, adjust

vector2 = pygame.Vector2


class Asteroid:
    def __init__(self):
        self.position = vector2(u.SCREEN_SIZE/2, u.SCREEN_SIZE/2)
        self.surface = self.prepare_surface()
        rotation = random.randint(0,360)
        self.velocity = u.ASTEROID_SPEED.rotate(rotation)

    def adjust(self, point):
        center_adjustment = vector2(4, 4)
        return (point + center_adjustment) * 16

    def move(self, dt):
        self.position += self.velocity*dt
        self.position.x = self.position.x % u.SCREEN_SIZE
        self.position.y = self.position.y % u.SCREEN_SIZE

    def prepare_surface(self):
        surface = pygame.Surface((128, 128))
        surface.set_colorkey((0, 0, 0))
        adjusted = list(map(adjust, raw_rocks[0], repeat(vector2(4,4)), repeat(16)))
        pygame.draw.lines(surface, "white", False, adjusted, 3)
        return surface

    def draw(self, screen):
        half = vector2(self.surface.get_size()) / 2
        screen.blit(self.surface, self.position - half)
