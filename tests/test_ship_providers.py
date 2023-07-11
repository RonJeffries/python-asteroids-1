from ShipProvider import SinglePlayerShipProvider
from fleets import Fleets
from tests.tools import FI


class TestShipProviders:
    def test_single_provider(self):
        fleets = Fleets()
        fi = FI(fleets)
        provider = SinglePlayerShipProvider(4)
        assert provider.ships_available(0) == 4

