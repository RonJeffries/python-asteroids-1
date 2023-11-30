from invaders.bitmap_maker import BitmapMaker


class Sprite:
    def __init__(self, surfaces):
        self._surfaces = surfaces


class TestSprite:
    def test_exists(self):
        maps = BitmapMaker.instance().squiggles
        squiggles = Sprite(maps)
        assert squiggles._surfaces == maps