from asteroid import Asteroid
from explosion import Explosion
from fleets import Fleets
from flyer import Flyer
from fragment import Fragment
from game_over import GameOver
from invaderfleet import InvaderFleet
from missile import Missile
from pygame import Vector2
from saucer import Saucer
from saucermaker import SaucerMaker
from score import Score
from scorekeeper import ScoreKeeper
from ship import Ship
from shipmaker import ShipMaker
from signal import Signal
from tests.tools import FI, BeginChecker, EndChecker
from thumper import Thumper
from wavemaker import WaveMaker
import coin


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
            Asteroid, BeginChecker, EndChecker,
            Fragment, GameOver, InvaderFleet, Missile, Saucer, SaucerMaker,
            Score, ScoreKeeper, Ship, ShipMaker, Signal, Thumper, WaveMaker}

    def test_no_unchecked_classes(self):
        # if this fails, we need to update `all_known_flyer_subclasses`
        # and re-verify the coin tests to be sure they don't need updating
        subs = set(Flyer.__subclasses__())
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

