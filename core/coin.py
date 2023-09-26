from pygame import Vector2

from invaders.bumper import Bumper
from asteroids.game_over import GameOver
from invaders.invader_score import InvaderScoreKeeper
from invaders.invaderfleet import InvaderFleet
from invaders.playermaker import PlayerMaker
from invaders.reserveplayer import ReservePlayer
from asteroids.saucermaker import SaucerMaker
from asteroids.scorekeeper import ScoreKeeper
from invaders.shield import Shield
from asteroids.shipmaker import ShipMaker
from invaders.shotcontroller import ShotController
from asteroids.thumper import Thumper
from invaders.top_bumper import TopBumper
from asteroids.wavemaker import WaveMaker


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
    left_bumper = 64
    fleets.append(Bumper(left_bumper, -1))
    fleets.append(Bumper(960, +1))
    fleets.append(TopBumper())
    fleets.append(InvaderFleet())
    fleets.append(PlayerMaker())
    fleets.append(ShotController())
    fleets.append(InvaderScoreKeeper())
    for i in range(3):
        fleets.append(ReservePlayer(i))
    half_width = 88 / 2
    spacing = 198
    step = 180
    for i in range(4):
        place = Vector2(half_width + spacing + i*step, 800-16)
        fleets.append(Shield(place))


def _append_common_elements(fleets):
    fleets.append(SaucerMaker())
    fleets.append(ScoreKeeper(0))
    fleets.append(Thumper())

