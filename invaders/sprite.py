import pygame
from pygame import Vector2

from invaders.bitmap_maker import BitmapMaker


class Sprite:
    def __init__(self, surfaces):
        self._surfaces = surfaces
        self._masks = [pygame.mask.from_surface(surface) for surface in self._surfaces]
        self._rectangle = self._surfaces[0].get_rect()
        self._frame_number = 0

    @classmethod
    def player_shot(cls):
        return cls((BitmapMaker.instance().player_shot, ))

    @property
    def mask(self):
        return self._masks[self._frame_number]

    @property
    def position(self):
        return Vector2(self.rectangle.center)

    @position.setter
    def position(self, value):
        self.rectangle.center = value

    @property
    def rectangle(self):
        return self._rectangle

    @property
    def surface(self):
        return self._surfaces[self._frame_number]

    def next_frame(self):
        self._frame_number = (self._frame_number + 1) % len(self._surfaces)

    def draw(self, screen):
        screen.blit(self.surface, self.rectangle)
