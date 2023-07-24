from asteroid import Asteroid
from explosion import Explosion
from flyer import Flyer
from fragment import Fragment
from game_over import GameOver
from missile import Missile
from saucer import Saucer
from saucermaker import SaucerMaker
from score import Score
from scorekeeper import ScoreKeeper
from ship import Ship
from raw_object_points import ShipMaker
from signal import Signal
from thumper import Thumper
from wavemaker import WaveMaker


class FleetsInspector:
    def __init__(self, fleets):
        self.fleets = fleets

    def all_classes(self):
        return set(map(lambda flyer: flyer.__class__, self.fleets.flyers))

    def select(self, condition):
        return self.fleets.select(condition)

    def select_class(self, klass):
        return self.select(lambda a: isinstance(a, klass))

    @property
    def asteroids(self):
        return self.select_class(Asteroid)

    @property
    def explosions(self):
        return self.select_class(Explosion)


    @property
    def fragments(self):
        return self.select_class(Fragment)

    @property
    def game_over(self):
        return self.select_class(GameOver)

    @property
    def missiles(self):
        return self.select_class(Missile)

    @property
    def saucers(self):
        return self.select_class(Saucer)

    @property
    def saucermakers(self):
        return self.select_class(SaucerMaker)

    @property
    def scorekeepers(self):
        return self.select_class(ScoreKeeper)

    @property
    def shipmakers(self):
        return self.select_class(ShipMaker)

    @property
    def signals(self):
        return self.select_class(Signal)

    @property
    def thumpers(self):
        return self.select_class(Thumper)

    @property
    def wavemakers(self):
        return self.select_class(WaveMaker)

    @property
    def scorekeeper(self):
        keepers = self.scorekeepers
        if keepers:
            return keepers[0]
        else:
            return ScoreKeeper()

    @property
    def score(self):
        return self.scorekeeper.score

    @property
    def scores(self):
        return self.select(lambda s: isinstance(s, Score))

    @property
    def ships(self):
        return self.select(lambda s: isinstance(s, Ship))


FI = FleetsInspector


class BeginChecker(Flyer):
    def __init__(self):
        self.triggered = False

    def tick(self, delta_time, fleets):
        pass

    def draw(self, screen):
        pass

    def interact_with(self, other, fleets):
        pass

    def begin_interactions(self, fleets):
        self.triggered = True

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass


class EndChecker(Flyer):
    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass

    def __init__(self):
        self.triggered = False

    def tick(self, delta_time, fleets):
        pass

    def draw(self, screen):
        pass

    def interact_with(self, other, fleets):
        pass

    def end_interactions(self, fleets):
        self.triggered = True


