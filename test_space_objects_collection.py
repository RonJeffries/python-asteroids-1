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

    def test_access(self):
        asteroids = ["asteroid"]
        missiles = ["missile"]
        saucers = ["saucer"]
        saucer_missiles = ["saucer_missile"]
        ships = ["ship"]
        space_objects = SpaceObjects(asteroids, missiles, saucers, saucer_missiles, ships)
        assert space_objects.asteroids == asteroids
        assert space_objects.missiles == missiles
        assert space_objects.saucers == saucers
        assert space_objects.saucer_missiles == saucer_missiles
        assert space_objects.ships == ships
