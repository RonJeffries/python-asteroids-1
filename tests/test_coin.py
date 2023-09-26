from asteroids.asteroid import Asteroid
from invaders.bumper import Bumper
from asteroids.explosion import Explosion
from core.fleets import Fleets
from flyer import AsteroidFlyer
from asteroids.fragment import Fragment
from asteroids.game_over import GameOver
from invaders.invader_player import InvaderPlayer
from invaders.invaderfleet import InvaderFleet
from asteroids.missile import Missile
from pygame import Vector2
from asteroids.saucer import Saucer
from asteroids.saucermaker import SaucerMaker
from asteroids.score import Score
from asteroids.scorekeeper import ScoreKeeper
from asteroids.ship import Ship
from asteroids.shipmaker import ShipMaker
from asteroids.signal import Signal
from tests.tools import FI, BeginChecker, EndChecker
from asteroids.thumper import Thumper
from asteroids.wavemaker import WaveMaker
from core import coin


class TestCoin:

    # def test_make_list(self):
    #     all_classes = Flyer.__subclasses__()
    #     names = list(map(lambda k: k.__name__, all_classes))
    #     names.sort()
    #     s = ""
    #     for name in names:
    #         s += name + ", "
    #     print(s)
    #     assert s == "hello"

    @staticmethod
    def all_known_flyer_subclasses():
        return {
            Asteroid, BeginChecker, Bumper, EndChecker,
            Fragment, GameOver, InvaderFleet, InvaderPlayer, Missile, Saucer, SaucerMaker,
            Score, ScoreKeeper, Ship, ShipMaker, Signal, Thumper, WaveMaker}

    # @pytest.mark.skip("needs updating")
    def test_no_unchecked_classes(self):
        # if this fails, we need to update `all_known_flyer_subclasses`
        # and re-verify the coin tests to be sure they don't need updating
        subs = set(AsteroidFlyer.__subclasses__())
        assert not subs - self.all_known_flyer_subclasses()

    def test_slug(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(Asteroid())
        coin.slug(fleets)
        desired = {GameOver, SaucerMaker, ScoreKeeper, Thumper, WaveMaker}
        undesired = fi.all_classes() - desired
        assert not undesired
        for klass in desired:
            assert fi.select_class(klass)

    def test_quarter(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(Asteroid())
        coin.quarter(fleets)
        desired = {SaucerMaker, ScoreKeeper, ShipMaker, Thumper, WaveMaker}
        undesired = fi.all_classes() - desired
        assert not undesired
        for klass in desired:
            assert fi.select_class(klass)

    def test_no_asteroids(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(Asteroid())
        coin.no_asteroids(fleets)
        desired = {SaucerMaker, ScoreKeeper, ShipMaker, Thumper}
        undesired = fi.all_classes() - desired
        assert not undesired
        for klass in desired:
            assert fi.select_class(klass)

    def test_saucer_explosion(self):
        fleets = Fleets()
        fi = FI(fleets)
        pos = Vector2(100, 100)
        Explosion.from_saucer(pos, fleets)
        assert len(fi.fragments) == 7

    def test_ship_explosion(self):
        fleets = Fleets()
        fi = FI(fleets)
        pos = Vector2(100, 100)
        Explosion.from_ship(pos, fleets)
        assert len(fi.fragments) == 7

