import u
from ShipProvider import SinglePlayerShipProvider, TwoPlayerShipProvider
from fleets import Fleets
from ship import Ship
from signal import Signal
from tests.tools import FI


class TestShipProviders:
    def test_single_provider(self):
        provider = SinglePlayerShipProvider(4)
        assert provider.ships_available(u.PLAYER_ZERO) == 4
        for i in range(0, 4):
            assert provider.ships_available(u.PLAYER_ZERO) == 4 - i
            items = provider.provide()
            ship = next(s for s in items if isinstance(s, Ship))
            assert ship.position == u.CENTER
            signal = next(s for s in items if isinstance(s, Signal))
            assert signal.signal == u.PLAYER_ZERO
        assert provider.ships_available(u.PLAYER_ZERO) == 0
        assert not provider.provide()

    def test_single_add(self):
        provider = SinglePlayerShipProvider(4)
        provider.add_ship(u.PLAYER_ZERO)
        assert provider.ships_available(u.PLAYER_ZERO) == 5

    def test_two_player(self):
        provider = TwoPlayerShipProvider(2)
        assert provider.ships_available(u.PLAYER_ZERO) == 2
        assert provider.ships_available(u.PLAYER_ONE) == 2

    def test_one_ship_for_each(self):
        provider = TwoPlayerShipProvider(1)
        items = provider.provide()
        ship = next(s for s in items if isinstance(s, Ship))
        assert ship.position == u.CENTER
        signal = next(s for s in items if isinstance(s, Signal))
        assert signal.signal == u.PLAYER_ZERO
        items = provider.provide()
        ship = next(s for s in items if isinstance(s, Ship))
        assert ship.position == u.CENTER
        signal = next(s for s in items if isinstance(s, Signal))
        assert signal.signal == u.PLAYER_ONE
        assert not provider.ships_available(u.PLAYER_ZERO)
        assert not provider.ships_available(u.PLAYER_ONE)
        assert not provider.provide()

