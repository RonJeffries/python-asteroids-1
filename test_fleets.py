import pytest

from fleets import Fleets
from fleet import Fleet


class FakeFlyer:
    def __init__(self):
        pass

    def control_motion(self, delta_time):
        pass

    def move(self, delta_time, fleet):
        pass

    def tick(self, _delta_time, _fleet, _fleets):
        return True


class TestFleets:
    def test_creation(self):
        asteroids = ["asteroid"]
        missiles = ["missile"]
        saucers = ["saucer"]
        saucer_missiles = ["saucer_missile"]
        ships = ["ship"]
        fleets = Fleets(asteroids, missiles, saucers, saucer_missiles, ships)
        assert fleets

    def test_access(self):
        asteroids = ["asteroid"]
        missiles = ["missile"]
        saucers = ["saucer"]
        saucer_missiles = ["saucer_missile"]
        ships = ["ship"]
        fleets = Fleets(asteroids, missiles, saucers, saucer_missiles, ships)
        assert fleets.asteroids == asteroids
        assert fleets.missiles == missiles
        assert fleets.saucers == saucers
        # assert fleets.saucer_missiles == saucer_missiles
        assert fleets.ships == ships

    def test_fleet_creation(self):
        asteroids = ["asteroid"]
        fleet = Fleet(asteroids)
        assert fleet

    def test_fleets_tick(self):
        asteroids = [FakeFlyer()]
        missiles = [FakeFlyer()]
        saucers = [FakeFlyer()]
        saucer_missiles = [FakeFlyer()]
        ships = [FakeFlyer()]
        fleets = Fleets(asteroids, missiles, saucers, saucer_missiles, ships)
        result = fleets.tick(0.1)
        assert result

