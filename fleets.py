# SpaceObjects
from itertools import chain
import u
from asteroid import Asteroid
from fleet import Fleet
from missile import Missile
from scorekeeper import ScoreKeeper
from sounds import player
from thumper import Thumper


class Fleets:
    ships_remaining = u.SHIPS_PER_QUARTER

    def __init__(self, asteroids=(), missiles=(), saucers=(), saucer_missiles=(), ships=()):
        self.fleets = dict(
            saucers=Fleet([]),
            ships=Fleet([]),
            flyers=Fleet([]))
        for asteroid in asteroids:
            self.add_asteroid(asteroid)
        for missile in missiles:
            self.add_missile(missile)
        for saucer in saucers:
            self.add_saucer(saucer)
        for saucer_missile in saucer_missiles:
            self.add_saucer_missile(saucer_missile)
        for ship in ships:
            self.add_ship(ship)
        self.thumper = Thumper(self.beat1, self.beat2)

    @property
    def all_objects(self):
        return list(chain(*self.fleets.values()))

    @property
    def _asteroids(self):
        return self.select(lambda a: isinstance(a, Asteroid))

    @property
    def missiles(self):
        return self.select(lambda m: isinstance(m, Missile))

    @property
    def saucers(self):
        return self.fleets["saucers"]

    @property
    def saucer_missiles(self):
        return self.select(lambda m: isinstance(m, Missile) and m.is_saucer_missile)

    @property
    def testing_only_score(self):
        keeper = next((k for k in self.flyers if isinstance(k, ScoreKeeper)), ScoreKeeper())
        return keeper.score

    @property
    def ships(self):
        return self.fleets["ships"]

    @property
    def flyers(self):
        return self.fleets["flyers"]

    # adds and removes

    def add_asteroid(self, asteroid):
        self.add_flyer(asteroid)

    def remove_asteroid(self, asteroid):
        self.remove_flyer(asteroid)

    def add_flyer(self, flyer):
        self.flyers.append(flyer)

    def remove_flyer(self, flyer):
        self.flyers.remove(flyer)

    def add_missile(self, missile):
        self.add_flyer(missile)

    def remove_missile(self, missile):
        self.flyers.remove(missile)

    def add_saucer(self, saucer):
        self.saucers.append(saucer)
    # no remove

    def remove_saucer(self, saucer):
        self.saucers.remove(saucer)

    def add_saucer_missile(self, missile):
        self.add_flyer(missile)

    def remove_saucer_missile(self, missile):
        self.remove_flyer(missile)

    def add_score(self, score):
        self.flyers.append(score)

    def remove_score(self, score):
        self.flyers.remove(score)

    def add_scorekeeper(self, scorekeeper):
        self.flyers.append(scorekeeper)

    def add_ship(self, ship):
        self.ships.append(ship)

    def remove_ship(self, ship):
        self.ships.remove(ship)

    def add_wavemaker(self, wavemaker):
        self.flyers.append(wavemaker)

    @staticmethod
    def beat1():
        player.play("beat1")

    @staticmethod
    def beat2():
        player.play("beat2")

    def clear(self):
        for fleet in self.fleets.values():
            fleet.clear()

    def count(self, condition):
        return len(self.select(condition))

    def draw(self, screen):
        for fleet in self.fleets.values():
            fleet.draw(screen)

    def select(self, condition):
        return [flyer for flyer in self.all_objects if condition(flyer)]

    def tick(self, delta_time):
        if self._asteroids and self.ships:
            self.thumper.tick(delta_time)
        else:
            self.thumper.reset()
        for fleet in self.fleets.values():
            fleet.tick(delta_time, self)

    def begin_interactions(self):
        for flyer in self.all_objects:
            flyer.begin_interactions(self)

    def end_interactions(self):
        for flyer in self.all_objects:
            flyer.end_interactions(self)
