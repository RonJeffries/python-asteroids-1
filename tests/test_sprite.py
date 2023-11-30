import pygame
from pygame import Mask, Vector2

from invaders.bitmap_maker import BitmapMaker


class Sprite:
    def __init__(self, surfaces):
        self._surfaces = surfaces
        self._masks = [pygame.mask.from_surface(surface) for surface in self._surfaces]
        self._rectangle = self._surfaces[0].get_rect()

    @property
    def rectangle(self):
        return self._rectangle

    @property
    def position(self):
        return Vector2(self.rectangle.center)

    @position.setter
    def position(self, value):
        self.rectangle.center = value


class TestSprite:
    def test_creation(self):
        maps = BitmapMaker.instance().squiggles
        squiggles = Sprite(maps)
        assert squiggles._surfaces == maps
        assert squiggles.rectangle == pygame.Rect(0, 0, 12, 32)
        assert isinstance(squiggles._masks[0], Mask)

    def test_position(self):
        maps = BitmapMaker.instance().squiggles
        squiggles = Sprite(maps)
        assert squiggles.position == Vector2(6, 16)
        squiggles.position = Vector2(100, 200)
        assert squiggles.position == Vector2(100, 200)

