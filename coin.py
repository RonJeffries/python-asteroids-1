from game_over import GameOver
from saucermaker import SaucerMaker
from scorekeeper import ScoreKeeper
from shipmaker import ShipMaker
from thumper import Thumper
from wavemaker import WaveMaker


class Coin:

    @classmethod
    def quarter(cls, fleets=None):
        coin = cls(True, True)
        if fleets:
            coin.populate(fleets)
        return coin

    @classmethod
    def slug(cls, fleets=None):
        coin = cls(False, True)
        if fleets:
            coin.populate(fleets)
        return coin

    @classmethod
    def no_asteroids(cls, fleets=None):
        coin = cls(True, False)
        if fleets:
            coin.populate(fleets)
        return coin

    def __init__(self, is_quarter=True, want_asteroids=True):
        self.is_quarter = is_quarter
        self.want_asteroids = want_asteroids

    def populate(self, fleets):
        fleets.clear()
        fleets.append(SaucerMaker())
        fleets.append(ScoreKeeper())
        fleets.append(Thumper())
        if self.want_asteroids:
            fleets.append(WaveMaker())
        fleets.append(ShipMaker() if self.is_quarter else GameOver())
