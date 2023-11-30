import pygame
from pygame import Vector2


class Sprite:
    def __init__(self, surfaces):
        self._surfaces = surfaces
        self._masks = [pygame.mask.from_surface(surface) for surface in self._surfaces]
        self._rectangle = self._surfaces[0].get_rect()

    @property
    def mask(self):
        return self._masks[0]

    @property
    def rectangle(self):
        return self._rectangle

    @property
    def position(self):
        return Vector2(self.rectangle.center)

    @position.setter
    def position(self, value):
        self.rectangle.center = value

    def draw(self, screen):
        screen.blit(self._surfaces[0], self.rectangle)
