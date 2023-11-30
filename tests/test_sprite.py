import pygame
from pygame import Mask

from invaders.bitmap_maker import BitmapMaker


class Sprite:
    def __init__(self, surfaces):
        self._surfaces = surfaces
        self._masks = [pygame.mask.from_surface(surface) for surface in self._surfaces]
        self._rectangle = self._surfaces[0].get_rect()

    @property
    def rectangle(self):
        return self._rectangle


class TestSprite:
    def test_exists(self):
        maps = BitmapMaker.instance().squiggles
        squiggles = Sprite(maps)
        assert squiggles._surfaces == maps
        assert squiggles.rectangle == pygame.Rect(0, 0, 12, 32)
        assert isinstance(squiggles._masks[0], Mask)
