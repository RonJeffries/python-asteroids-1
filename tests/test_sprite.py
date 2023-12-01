import pygame
from pygame import Mask, Vector2

from invaders.bitmap_maker import BitmapMaker
from invaders.sprite import Sprite


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

    def test_animation(self):
        maps = BitmapMaker.instance().squiggles
        squiggles = Sprite(maps)
        assert squiggles._frame_number == 0
        for i in range(len(maps)):
            assert squiggles.mask == squiggles._masks[i]
            assert squiggles.surface == squiggles._surfaces[i]
            squiggles.next_frame()
        assert squiggles._frame_number == 0


