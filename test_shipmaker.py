import u
from fleets import Fleets
from interactor import Interactor
from shipmaker import ShipMaker
from test_interactions import FI


class TestShipMaker:
    def test_exists(self):
        ShipMaker()

    def test_creates_ship(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.add_flyer(ShipMaker())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        assert not fi.ships
        fleets.tick(u.SHIP_EMERGENCE_TIME)
        assert fi.ships
