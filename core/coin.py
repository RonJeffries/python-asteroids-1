from asteroids.game_over import GameOver
from asteroids.saucermaker import SaucerMaker
from asteroids.scorekeeper import ScoreKeeper
from asteroids.shipmaker import ShipMaker
from asteroids.thumper import Thumper
from asteroids.wavemaker import WaveMaker
from invaders.bumper import Bumper
from invaders.invader_score import InvaderScoreKeeper
from invaders.invaderfleet import InvaderFleet
from invaders.invaders_game_over import InvadersGameOver
from invaders.invaders_saucer_maker import InvadersSaucerMaker
from invaders.playermaker import PlayerMaker
from invaders.reserveplayer import ReservePlayer
from invaders.roadfurniture import RoadFurniture
from invaders.shotcontroller import ShotController
from invaders.timecapsule import TimeCapsule
from invaders.top_bumper import TopBumper
from pygame import Vector2
import u
from invaders.robotplayer import RobotPlayer


def quarter(fleets):
    fleets.clear()
    fleets.append(WaveMaker())
    fleets.append(ShipMaker(1))
    _append_common_asteroids_elements(fleets)


def two_player(fleets):
    fleets.clear()
    fleets.append(WaveMaker())
    fleets.append(ShipMaker(2))
    fleets.append(ScoreKeeper(1))
    _append_common_asteroids_elements(fleets)


def slug(fleets):
    fleets.clear()
    fleets.append(WaveMaker())
    fleets.append(GameOver())
    _append_common_asteroids_elements(fleets)


def no_asteroids(fleets):
    fleets.clear()
    fleets.append(ShipMaker(1))
    _append_common_asteroids_elements(fleets)


def invaders(fleets):
    fleets.clear()
    left_bumper = u.BUMPER_LEFT
    fleets.append(Bumper(left_bumper, -1))
    fleets.append(Bumper(u.BUMPER_RIGHT, +1))
    fleets.append(TopBumper())
    fleets.append(InvaderFleet())
    fleets.append(PlayerMaker())
    fleets.append(ShotController())
    fleets.append(InvaderScoreKeeper())
    fleets.append(RoadFurniture.bottom_line())
    fleets.append(TimeCapsule(10, InvadersSaucerMaker()))
    for i in range(3):
        fleets.append(ReservePlayer(i))
    half_width = 88 / 2
    spacing = 198
    step = 180
    for i in range(4):
        place = Vector2(half_width + spacing + i * step, u.SHIELD_Y)
        fleets.append(RoadFurniture.shield(place))


def _append_common_asteroids_elements(fleets):
    fleets.append(SaucerMaker())
    fleets.append(ScoreKeeper(0))
    fleets.append(Thumper())
