from game_over import GameOver
from saucermaker import SaucerMaker
from scorekeeper import ScoreKeeper
from shipmaker import ShipMaker
from thumper import Thumper
from wavemaker import WaveMaker


class Coin:

    @classmethod
    def quarter(cls, fleets):
        cls.create_common_elements(fleets)
        fleets.append(WaveMaker())
        fleets.append(ShipMaker())

    @classmethod
    def slug(cls, fleets):
        cls.create_common_elements(fleets)
        fleets.append(WaveMaker())
        fleets.append(GameOver())

    @classmethod
    def no_asteroids(cls, fleets):
        cls.create_common_elements(fleets)
        fleets.append(ShipMaker())

    @classmethod
    def create_common_elements(cls, fleets):
        fleets.clear()
        fleets.append(SaucerMaker())
        fleets.append(ScoreKeeper())
        fleets.append(Thumper())
