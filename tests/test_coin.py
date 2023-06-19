from coin import Coin
from fleets import Fleets
from tests.test_interactions import FI


class TestCoin:

    def test_slug(self):
        fleets = Fleets()
        fi = FI(fleets)
        Coin.slug(fleets)
        assert fi.saucermakers
        assert fi.scorekeepers
        assert fi.thumpers
        assert fi.wavemakers
        assert not fi.shipmakers
