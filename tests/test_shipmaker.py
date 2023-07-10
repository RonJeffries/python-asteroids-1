from pygame import Vector2

import u
from asteroid import Asteroid
from fleets import Fleets
from interactor import Interactor
from missile import Missile
from saucer import Saucer
from shipmaker import ShipMaker
from tests.tools import FI


class TestShipMaker:
    def test_exists(self):
        ShipMaker(1)

    def test_creates_ship(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(ShipMaker(1))
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        assert not fi.ships
        fleets.tick(u.SHIP_EMERGENCE_TIME)
        assert fi.ships

    def test_unsafe_because_missile(self):
        missile = Missile("ship", u.CENTER, Vector2(0, 0))
        fleets = Fleets()
        fleets.append(ShipMaker(1))
        interactor = Interactor(fleets)
        fi = FI(fleets)
        interactor.perform_interactions()
        fleets.tick(u.SHIP_EMERGENCE_TIME - 1)
        assert not fi.ships
        fleets.append(missile)
        interactor.perform_interactions()
        fleets.tick(1)
        assert not fi.ships
        for missile in fi.missiles:
            fleets.remove(missile)
        interactor.perform_interactions()
        fleets.tick(0.001)
        assert fi.ships

    def test_unsafe_because_saucer(self):
        fleets = Fleets()
        fleets.append(ShipMaker(1))
        interactor = Interactor(fleets)
        fi = FI(fleets)
        interactor.perform_interactions()
        fleets.tick(u.SHIP_EMERGENCE_TIME - 1)
        assert not fi.ships
        fleets.append(Saucer.large())
        interactor.perform_interactions()
        fleets.tick(1)
        assert not fi.ships
        for missile in fi.missiles:
            fleets.remove(missile)
        interactor.perform_interactions()
        fleets.tick(0.001)
        assert not fi.ships
        for saucer in fi.saucers:
            fleets.remove(saucer)
        interactor.perform_interactions()
        fleets.tick(0.001)
        assert fi.ships

    def test_unsafe_because_asteroid(self):
        fleets = Fleets()
        fleets.append(ShipMaker(1))
        interactor = Interactor(fleets)
        fi = FI(fleets)
        asteroid = Asteroid()
        asteroid.move_to(u.CENTER + Vector2(u.SAFE_EMERGENCE_DISTANCE - 0.1, 0))
        asteroid._location.velocity = Vector2(0, 0)
        fleets.append(asteroid)
        assert not fi.ships
        interactor.perform_interactions()
        fleets.tick(u.SHIP_EMERGENCE_TIME)
        assert not fi.ships
        asteroid.move_to(u.CENTER + Vector2(u.SAFE_EMERGENCE_DISTANCE + 0.1, 0))
        interactor.perform_interactions()
        fleets.tick(0.001)
        assert fi.ships

    def test_can_run_out_of_ships(self):
        fleets = Fleets()
        fleets.append(ShipMaker(1))
        interactor = Interactor(fleets)
        fi = FI(fleets)
        for _ in range(4):
            interactor.perform_interactions()
            fleets.tick(u.SHIP_EMERGENCE_TIME)
            assert fi.ships
            assert not fi.game_over
            for ship in fi.ships:
                fleets.remove(ship)
        interactor.perform_interactions()
        fleets.tick(u.SHIP_EMERGENCE_TIME)
        assert not fi.ships
        assert fi.game_over

    def test_unequal_ship_count(self):
        fleets = Fleets()
        fi = FI(fleets)
        maker = ShipMaker(2)
        maker._ships_remaining = [1, 3]

        self.make_ship_for_player(0, fi, fleets, maker)
        assert maker._next_player == 1
        self.make_ship_for_player(1, fi, fleets, maker)
        self.make_ship_for_player(1, fi, fleets, maker)
        self.make_ship_for_player(1, fi, fleets, maker)

        assert not maker.ships_remain()

    @staticmethod
    def make_ship_for_player(player, fi, fleets, maker):
        assert maker.ships_remain()
        maker.rez_available_ship(fleets)
        signal = fi.signals[0]
        assert signal.signal == player
        fleets.remove(signal)


