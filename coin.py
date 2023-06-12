from flyer import Flyer
from game_over import GameOver
from saucermaker import SaucerMaker
from scorekeeper import ScoreKeeper
from shipmaker import ShipMaker
from thumper import Thumper
from wavemaker import WaveMaker


class Coin(Flyer):
    @classmethod
    def quarter(cls):
        return cls(True)

    @classmethod
    def slug(cls):
        return cls(False)

    def __init__(self, is_quarter=True):
        self.is_quarter = is_quarter

    def interact_with(self, other, fleets):
        other.interact_with_coin(self, fleets)

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleets):
        fleets.clear()
        fleets.add_flyer(SaucerMaker())
        fleets.add_flyer(ScoreKeeper())
        fleets.add_flyer(Thumper())
        fleets.add_flyer(WaveMaker())
        fleets.add_flyer(ShipMaker() if self.is_quarter else GameOver())
