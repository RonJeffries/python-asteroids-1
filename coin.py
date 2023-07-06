from game_over import GameOver
from saucermaker import SaucerMaker
from scorekeeper import ScoreKeeper
from shipmaker import ShipMaker
from thumper import Thumper
from wavemaker import WaveMaker


def quarter(fleets):
    fleets.clear()
    fleets.append(WaveMaker())
    fleets.append(ShipMaker())
    _append_common_elements(fleets)


def slug(fleets):
    fleets.clear()
    fleets.append(WaveMaker())
    fleets.append(GameOver())
    _append_common_elements(fleets)


def no_asteroids(fleets):
    fleets.clear()
    fleets.append(ShipMaker())
    _append_common_elements(fleets)


def _append_common_elements(fleets):
    fleets.append(SaucerMaker())
    fleets.append(ScoreKeeper())
    fleets.append(Thumper())

