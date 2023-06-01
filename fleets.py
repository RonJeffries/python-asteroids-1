# SpaceObjects
import u
from asteroid import Asteroid
from fleet import Fleet
from ship import Ship
from sounds import player
from thumper import Thumper


class Fleets:
    ships_remaining = u.SHIPS_PER_QUARTER

    def __init__(self, asteroids=(), missiles=(), saucers=(), saucer_missiles=(), ships=()):
        self.flyers = Fleet([])
        for asteroid in asteroids:
            self.add_flyer(asteroid)
        for missile in missiles:
            self.add_flyer(missile)
        for saucer in saucers:
            self.add_flyer(saucer)
        for saucer_missile in saucer_missiles:
            self.add_flyer(saucer_missile)
        for ship in ships:
            self.add_flyer(ship)

    @property
    def all_objects(self):
        return self.flyers

    @property
    def _asteroids(self):
        return self.select(lambda a: isinstance(a, Asteroid))

    @property
    def _ships(self):
        return self.select(lambda s: isinstance(s, Ship))

    # adds and removes

    def add_flyer(self, flyer):
        self.flyers.append(flyer)

    def remove_flyer(self, flyer):
        self.flyers.remove(flyer)

    @staticmethod
    def beat1():
        player.play("beat1")

    @staticmethod
    def beat2():
        player.play("beat2")

    def clear(self):
        self.flyers.clear()

    def draw(self, screen):
        self.flyers.draw(screen)

    def move(self, delta_time):
        self.flyers.move(delta_time, self)

    def select(self, condition):
        return [flyer for flyer in self.all_objects if condition(flyer)]

    def tick(self, delta_time):
        self.flyers.tick(delta_time, self)

    def begin_interactions(self):
        for flyer in self.all_objects:
            flyer.begin_interactions(self)

    def end_interactions(self):
        for flyer in self.all_objects:
            flyer.end_interactions(self)
