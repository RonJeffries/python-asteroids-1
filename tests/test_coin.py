from asteroid import Asteroid
from explosion import Explosion
from fleets import Fleets
from itertools import accumulate
from pygame import Vector2

from flyer import Flyer
from fragment import Fragment
from game_over import GameOver
from missile import Missile
from saucer import Saucer
from saucermaker import SaucerMaker
from score import Score
from scorekeeper import ScoreKeeper
from ship import Ship
from shipmaker import ShipMaker
from tests.test_interactions import FI, BeginChecker, EndChecker
import coin
from thumper import Thumper
from wavemaker import WaveMaker


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

    def all_classes_except(self, classes):
        all_classes = self.all_known_classes()
        return [k for k in all_classes if k not in classes]

    def all_known_classes(self):
        return [
            Asteroid, BeginChecker, EndChecker,
            Fragment, GameOver, Missile, Saucer, SaucerMaker,
            Score, ScoreKeeper, Ship, ShipMaker, Thumper, WaveMaker]

    def test_slug(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(Asteroid())
        coin.slug(fleets)
        desired = [GameOver, SaucerMaker, ScoreKeeper, Thumper, WaveMaker]
        undesired = self.all_classes_except(desired)
        for klass in desired:
            assert fi.select_class(klass)
        for klass in undesired:
            assert not fi.select_class(klass)

    def test_quarter(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(Asteroid())
        coin.quarter(fleets)
        desired = [SaucerMaker, ScoreKeeper, ShipMaker, Thumper, WaveMaker]
        undesired = self.all_classes_except(desired)
        for klass in desired:
            assert fi.select_class(klass)
        for klass in undesired:
            assert not fi.select_class(klass)

    def test_no_asteroids(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(Asteroid())
        coin.no_asteroids(fleets)
        desired = [SaucerMaker, ScoreKeeper, ShipMaker, Thumper]
        undesired = self.all_classes_except(desired)
        for klass in desired:
            assert fi.select_class(klass)
        for klass in undesired:
            assert not fi.select_class(klass)

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

