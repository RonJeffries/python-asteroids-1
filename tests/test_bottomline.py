from pygame import Surface, Rect

from invaders.bottomline import BottomLine


class TestBottomLine:
    def test_exists(self):
        BottomLine()

    def test_rect(self):
        w = 960-128
        h = 4
        surface = Surface((w, h))
        rect = Rect(0, 0, w, h)
        assert surface.get_rect() == rect
