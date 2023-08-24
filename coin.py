from pygame import Vector2

import u
from bumper import Bumper
from game_over import GameOver
from invader_player import InvaderPlayer
from invaderfleet import InvaderFleet
from saucermaker import SaucerMaker
from scorekeeper import ScoreKeeper
from shield import Shield
from shipmaker import ShipMaker
from shotcontroller import ShotController
from thumper import Thumper
from top_bumper import TopBumper
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
    fleets.append(Bumper(64, -1))
    fleets.append(Bumper(960, +1))
    fleets.append(TopBumper())
    fleets.append(InvaderFleet())
    fleets.append(InvaderPlayer())
    fleets.append(ShotController())
    fleets.append(Shield(Vector2(100, 900)))


def _append_common_elements(fleets):
    fleets.append(SaucerMaker())
    fleets.append(ScoreKeeper(0))
    fleets.append(Thumper())

