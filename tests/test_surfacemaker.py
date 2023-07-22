from pygame import Vector2

from SurfaceMaker import SurfaceMaker


class TestSurfaceMaker:

    def test_fetch(self):
        maker = CachedMaker()
        make_count = 0

        def make(args):
            nonlocal make_count
            make_count += 1
            return "made {0}-{1}-{2}".format(args[0], args[1], args[2])

        made = maker.fetch("ship-5-7", make, "ship", 5, 7)
        assert made == "made ship-5-7"
        assert make_count == 1
        made = maker.fetch("ship-5-7", make, "ship", 5, 7)
        assert made == "made ship-5-7"
        assert make_count == 1

    def test_span(self):
        points = [Vector2(-3, 9), Vector2(2, 5)]
        span = SurfaceMaker.span(points)
        assert span == Vector2(5, 4)


class CachedMaker:
    def __init__(self):
        self.cache = dict()

    def fetch(self, key, action, *args):
        try:
            return self.cache[key]
        except KeyError:
            new_one = action(args)
            self.cache[key] = new_one
            return new_one


