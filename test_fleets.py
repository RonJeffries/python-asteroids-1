from pygame import Vector2

import u
from asteroid import Asteroid
from fleets import Fleets
from fleet import Fleet, ShipFleet
from missile import Missile
from test_interactions import FI


class FakeFlyer:
    def __init__(self):
        pass

    def control_motion(self, delta_time):
        pass

    def fire_if_possible(self, _delta_time, _saucer_missiles, _ships):
        pass

    def move(self, delta_time, fleet):
        pass

    @staticmethod
    def tick(_delta_time, _fleet, _fleets):
        pass


class TestFleets:
    def test_creation(self):
        asteroids = ["asteroid"]
        missiles = ["missile"]
        saucers = ["saucer"]
        saucer_missiles = ["saucer_missile"]
        ships = ["ship"]
        fleets = Fleets(asteroids, missiles, saucers, saucer_missiles, ships)
        assert fleets

    def test_fleet_creation(self):
        asteroids = ["asteroid"]
        fleet = Fleet(asteroids)
        assert fleet

    def test_saucer_spawn(self):
        fleets = Fleets()
        fleets.tick(0.1)
        assert not FI(fleets).saucers
        fleets.tick(u.SAUCER_EMERGENCE_TIME)
        assert FI(fleets).saucers

    def test_len_etc(self):
        saucer_missiles = []
        fleets = Fleets([], [], [], saucer_missiles, [])
        s_m_fleet = fleets.saucer_missiles
        assert len(s_m_fleet) == 0
        s_m_fleet.extend([1, 20, 300])
        assert len(s_m_fleet) == 3
        assert s_m_fleet[1] == 20

    def test_ship_rez(self):
        ShipFleet.rez_from_fleet = True
        fleets = Fleets()
        fi = FI(fleets)
        assert not fi.ships
        fleets.tick(0.1)
        assert not fi.ships
        fleets.tick(u.SHIP_EMERGENCE_TIME)
        assert fi.ships

    def test_unsafe_because_missile(self):
        ShipFleet.rez_from_fleet = True
        ships = []
        missile = Missile(u.CENTER, Vector2(0, 0), [0, 0, 0], [0, 0, 0])
        fleets = Fleets()
        fi = FI(fleets)
        assert not fi.ships
        fleets.tick(u.SHIP_EMERGENCE_TIME - 1)
        assert not fi.ships
        fleets.add_missile(missile)
        fleets.tick(1)
        assert not fi.ships
        for missile in fi.missiles:
            print("removing")
            fleets.remove_missile(missile)
        fleets.tick(0.001)
        assert fi.ships

    def test_unsafe_because_saucer_missile(self):
        fleets = Fleets()
        missile = Missile(u.CENTER, Vector2(0, 0), [0, 0, 0], [0, 0, 0])
        assert not FI(fleets).ships
        fleets.tick(u.SHIP_EMERGENCE_TIME - 1)
        fleets.add_saucer_missile(missile)
        fleets.tick(1)
        assert not FI(fleets).ships
        FI(fleets).clear_saucer_missiles()
        fleets.tick(0.001)
        assert FI(fleets).ships

    def test_unsafe_because_asteroid(self):
        fleets = Fleets()
        ShipFleet.rez_from_fleet = True
        asteroid = Asteroid()
        asteroid.move_to(u.CENTER + Vector2(u.SAFE_EMERGENCE_DISTANCE - 0.1, 0))
        asteroid._location.velocity = Vector2(0, 0)
        fleets.add_asteroid(asteroid)
        fi = FI(fleets)
        assert not fi.ships
        fleets.tick(u.SHIP_EMERGENCE_TIME)
        assert not fi.ships
        for asteroid in fi.asteroids:
            fleets.remove_asteroid(asteroid)
        fleets.tick(0.001)
        assert fi.ships

    def test_can_run_out_of_ships(self):
        ShipFleet.rez_from_fleet = True
        fleets = Fleets()
        fi = FI(fleets)
        ShipFleet.ships_remaining = 2
        fleets.tick(u.SHIP_EMERGENCE_TIME)
        assert fi.ships
        assert fleets.ships.ships_remaining == 1
        for ship in fi.ships:
            fleets.remove_ship(ship)
        fleets.tick(u.SHIP_EMERGENCE_TIME)
        assert fi.ships
        assert fleets.ships.ships_remaining == 0
        assert not fleets.ships.game_over
        for ship in fi.ships:
            fleets.remove_ship(ship)
        fleets.tick(u.SHIP_EMERGENCE_TIME)
        assert not fi.ships
        assert fleets.ships.game_over

