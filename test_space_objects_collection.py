import pytest

from spaceobjects import SpaceObjects


class TestSpaceObjectsCollection:
    def test_creation(self):
        asteroids = ["asteroid"]
        missiles = ["missile"]
        saucers = ["saucer"]
        saucer_missiles = ["saucer_missile"]
        ships = ["ship"]
        space_objects = SpaceObjects(asteroids, missiles, saucers,  saucer_missiles, ships)
