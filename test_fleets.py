import pytest

import u
from fleets import Fleets
from fleet import Fleet, SaucerFleet, AsteroidFleet


class FakeFlyer:
    def __init__(self):
        pass

    def control_motion(self, delta_time):
        pass

    def fire_if_possible(self, _delta_time, _saucer_missiles, _ships):
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
        assert fleets.asteroids.flyers == asteroids
        assert fleets.missiles.flyers == missiles
        assert fleets.saucers.flyers == saucers
        assert fleets.saucer_missiles.flyers == saucer_missiles
        assert fleets.ships.flyers == ships

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

    def test_saucer_spawn(self):
        saucers = []
        fleets = Fleets([], [], saucers, [], [])
        saucer_fleet = fleets.saucers
        saucer_fleet.tick(0.1, fleets)
        assert not saucers
        saucer_fleet.tick(u.SAUCER_EMERGENCE_TIME, fleets)
        assert saucers

    def test_len_etc(self):
        saucer_missiles = []
        fleets = Fleets([], [], [], saucer_missiles, [])
        s_m_fleet = fleets.saucer_missiles
        assert len(s_m_fleet) == 0
        s_m_fleet.extend([1, 20, 300])
        assert len(s_m_fleet) == 3
        assert s_m_fleet[1] == 20

    def test_asteroid_fleet_exists(self):
        asteroids = []
        fleet = AsteroidFleet(asteroids)

    def test_asteroid_wave(self):
        asteroids = []
        fleets = Fleets(asteroids, [], [], [], [])
        asteroid_fleet = fleets.asteroids
        assert isinstance(asteroid_fleet, AsteroidFleet)
        asteroid_fleet.tick(0.1, fleets)
        assert not asteroids
        asteroid_fleet.tick(u.ASTEROID_DELAY, fleets)
        assert len(asteroids) == 4
        asteroid_fleet.clear()
        asteroid_fleet.tick(u.ASTEROID_DELAY, fleets)
        assert len(asteroids) == 6
        asteroid_fleet.clear()
        asteroid_fleet.tick(u.ASTEROID_DELAY, fleets)
        assert len(asteroids) == 8
        asteroid_fleet.clear()
        asteroid_fleet.tick(u.ASTEROID_DELAY, fleets)
        assert len(asteroids) == 10
        asteroid_fleet.clear()
        asteroid_fleet.tick(u.ASTEROID_DELAY, fleets)
        assert len(asteroids) == 11
        asteroid_fleet.clear()
        asteroid_fleet.tick(u.ASTEROID_DELAY, fleets)
        assert len(asteroids) == 11



