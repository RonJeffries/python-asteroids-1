import pytest


class TestSurfaceMaker:
    def test_key(self):
        maker = CachedMaker()
        key = maker.key("ship", 5, 7)
        assert key == "ship-5-7"
        key = maker.key("asteroid")
        assert key == "asteroid-0-1"

    def test_fetch(self):
        maker = CachedMaker()
        make_count = 0

        def make(kind, shape, size):
            nonlocal make_count
            make_count += 1
            return "made {0}-{1}-{2}".format(kind, shape, size)

        made = maker.fetch("ship", 5, 7, make)
        assert made == "made ship-5-7"
        assert make_count == 1
        made = maker.fetch("ship", 5, 7, make)
        assert made == "made ship-5-7"
        assert make_count == 1


class CachedMaker:
    def __init__(self):
        self.cache = dict()

    def key(self, kind, shape=0, size=1):
        return "{0}-{1}-{2}".format(kind, shape, size)

    def fetch(self, kind, shape, size, action):
        key = self.key(kind, shape, size)
        cached = self.cache.get(key)
        if cached:
            return cached
        new_one = action(kind, shape, size)
        self.cache[key] = new_one
        return new_one

