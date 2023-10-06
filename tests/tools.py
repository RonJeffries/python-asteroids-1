from asteroids.asteroid import Asteroid
from asteroids.explosion import Explosion
from flyer import AsteroidFlyer
from asteroids.fragment import Fragment
from asteroids.game_over import GameOver
from invaders.invader_player import InvaderPlayer
from invaders.invader_score import InvaderScore
from invaders.invader_shot import InvaderShot
from asteroids.missile import Missile
from invaders.invaders_saucer import InvadersSaucer
from invaders.player_shot import PlayerShot
from invaders.reserveplayer import ReservePlayer
from asteroids.saucer import Saucer
from asteroids.saucermaker import SaucerMaker
from asteroids.score import Score
from asteroids.scorekeeper import ScoreKeeper
from asteroids.ship import Ship
from asteroids.shipmaker import ShipMaker
from asteroids.signal import Signal
from asteroids.thumper import Thumper
from asteroids.wavemaker import WaveMaker
from invaders.timecapsule import TimeCapsule


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
    def invader_players(self):
        return self.select_class(InvaderPlayer)

    @property
    def invader_saucers(self):
        return self.select_class(InvadersSaucer)

    @property
    def invader_shots(self):
        return self.select_class(InvaderShot)

    @property
    def missiles(self):
        return self.select_class(Missile)

    @property
    def player_shots(self):
        return self.select_class(PlayerShot)

    @property
    def reserve_players(self):
        return self.select_class(ReservePlayer)

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
    def time_capsules(self):
        return self.select_class(TimeCapsule)

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
        return self.select(lambda s: isinstance(s, Score) or isinstance(s, InvaderScore))

    @property
    def ships(self):
        return self.select(lambda s: isinstance(s, Ship))


FI = FleetsInspector


class BeginChecker(AsteroidFlyer):
    def interact_with_fragment(self, fragment, fleets):
        pass

    def interact_with_gameover(self, game_over, fleets):
        pass

    def interact_with_saucermaker(self, saucermaker, fleets):
        pass

    def interact_with_score(self, score, fleets):
        pass

    def interact_with_scorekeeper(self, scorekeeper, fleets):
        pass

    def interact_with_shipmaker(self, shipmaker, fleets):
        pass

    def interact_with_signal(self, signal, fleets):
        pass

    def interact_with_thumper(self, thumper, fleets):
        pass

    def interact_with_wavemaker(self, wavemaker, fleets):
        pass

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


class EndChecker(AsteroidFlyer):
    def interact_with_fragment(self, fragment, fleets):
        pass

    def interact_with_gameover(self, game_over, fleets):
        pass

    def interact_with_saucermaker(self, saucermaker, fleets):
        pass

    def interact_with_score(self, score, fleets):
        pass

    def interact_with_scorekeeper(self, scorekeeper, fleets):
        pass

    def interact_with_shipmaker(self, shipmaker, fleets):
        pass

    def interact_with_signal(self, signal, fleets):
        pass

    def interact_with_thumper(self, thumper, fleets):
        pass

    def interact_with_wavemaker(self, wavemaker, fleets):
        pass

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


class FakeFleets():
    def __init__(self):
        self.appends = []
        self.removes = []

    def append(self, thing):
        self.appends.append(thing)

    def remove(self, thing):
        self.removes.append(thing)

