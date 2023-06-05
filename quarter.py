from flyer import Flyer
from saucermaker import SaucerMaker
from scorekeeper import ScoreKeeper
from shipmaker import ShipMaker
from thumper import Thumper
from wavemaker import WaveMaker


class Quarter(Flyer):
    def __init__(self, amount=25):
        self.amount = amount

    def interact_with(self, other, fleets):
        other.interact_with_quarter(self, fleets)

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleets):
        fleets.clear()
        fleets.add_flyer(SaucerMaker())
        fleets.add_flyer(ScoreKeeper())
        fleets.add_flyer(Thumper())
        fleets.add_flyer(WaveMaker())
        if self.amount:
            fleets.add_flyer(ShipMaker())
