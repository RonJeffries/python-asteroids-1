from flyer import Flyer
from saucermaker import SaucerMaker
from scorekeeper import ScoreKeeper
from shipmaker import ShipMaker
from thumper import Thumper
from wavemaker import WaveMaker


class Quarter(Flyer):
    def interact_with(self, other, fleets):
        other.interact_with_quarter(self, fleets)

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleet, fleets):
        fleets.remove_flyer(self)
        fleets.add_flyer(SaucerMaker())
        fleets.add_flyer(ScoreKeeper(False))
        fleets.add_flyer(ShipMaker())
        fleets.add_flyer(Thumper())
        fleets.add_flyer(WaveMaker())
