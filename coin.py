from game_over import GameOver
from invaderfleet import InvaderFleet
from saucermaker import SaucerMaker
from scorekeeper import ScoreKeeper
from shipmaker import ShipMaker
from thumper import Thumper
from wavemaker import WaveMaker


def quarter(fleets):
    fleets.clear()
    fleets.append(WaveMaker())
    fleets.append(ShipMaker(1))
    _append_common_elements(fleets)


def two_player(fleets):
    fleets.clear()
    fleets.append(WaveMaker())
    fleets.append(ShipMaker(2))
    fleets.append(ScoreKeeper(1))
    _append_common_elements(fleets)


def slug(fleets):
    fleets.clear()
    fleets.append(WaveMaker())
    fleets.append(GameOver())
    _append_common_elements(fleets)


def no_asteroids(fleets):
    fleets.clear()
    fleets.append(ShipMaker(1))
    _append_common_elements(fleets)


def invaders(fleets):
    fleets.clear()
    fleets.append(InvaderFleet())


def _append_common_elements(fleets):
    fleets.append(SaucerMaker())
    fleets.append(ScoreKeeper(0))
    fleets.append(Thumper())

