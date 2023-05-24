# SpaceObjects
from itertools import chain

import pygame.mixer

import u
from fleet import ShipFleet, SaucerFleet, MissileFleet, Fleet
from sounds import player
from thumper import Thumper


class Fleets:
    def __init__(self, asteroids=None, missiles=None, saucers=None, saucer_missiles=None, ships=None):
        asteroids = asteroids if asteroids is not None else []
        missiles = missiles if missiles is not None else []
        saucers = saucers if saucers is not None else []
        saucer_missiles = saucer_missiles if saucer_missiles is not None else []
        ships = ships if ships is not None else []
        self.fleets = (
            Fleet(asteroids),
            MissileFleet(missiles, u.MISSILE_LIMIT),
            SaucerFleet(saucers),
            MissileFleet(saucer_missiles, u.SAUCER_MISSILE_LIMIT),
            ShipFleet(ships),
            Fleet([]),  # explosions not used
            Fleet([]))
        self.thumper = Thumper(self.beat1, self.beat2)
        self.score = 0

    @property
    def all_objects(self):
        return list(chain(*self.fleets))

    @property
    def asteroids(self):
        return self.fleets[0]

    @property
    def asteroid_count(self):
        return len(self.asteroids)

    @property
    def missiles(self):
        return self.fleets[1]

    @property
    def saucers(self):
        return self.fleets[2]

    @property
    def saucer_missiles(self):
        return self.fleets[3]

    @property
    def ships(self):
        return self.fleets[4]

    @property
    def explosions(self):
        return self.fleets[5]

    @property
    def others(self):
        return self.fleets[6]

    def add_asteroid(self, asteroid):
        self.asteroids.append(asteroid)

    def add_flyer(self, flyer):
        self.others.append(flyer)

    def remove_flyer(self, flyer):
        self.others.remove(flyer)

    def add_score(self, score):
        self.others.append(score)
        self.score += score.score

    def add_scorekeeper(self, scorekeeper):
        self.others.append(scorekeeper)

    def has_asteroid(self, asteroid):
        # this code violates the decentralized design
        # by asking a question of the Fleet.
        # Fix it up when we fold the fleet instances together.
        return asteroid in self.asteroids

    def remove_asteroid(self, asteroid):
        self.asteroids.remove(asteroid)

    def remove_missile(self, missile):
        self.missiles.remove(missile)

    def remove_saucer(self, saucer):
        self.saucers.remove(saucer)

    def remove_score(self, score):
        self.others.remove(score)

    def remove_ship(self, ship):
        self.ships.remove(ship)

    @staticmethod
    def beat1():
        player.play("beat1")

    @staticmethod
    def beat2():
        player.play("beat2")

    def clear(self):
        for fleet in self.fleets:
            fleet.clear()

    def draw(self, screen):
        for fleet in self.fleets:
            fleet.draw(screen)

    def explosion_at(self, position):
        self.explosions.explosion_at(position)

    def safe_to_emerge(self):
        if self.missiles:
            return False
        if self.saucer_missiles:
            return False
        return self.all_asteroids_are_away_from_center()

    def all_asteroids_are_away_from_center(self):
        for asteroid in self.asteroids:
            if asteroid.position.distance_to(u.CENTER) < u.SAFE_EMERGENCE_DISTANCE:
                return False
        return True

    def tick(self, delta_time):
        if self.asteroids and self.ships:
            self.thumper.tick(delta_time)
        else:
            self.thumper.reset()
        for fleet in self.fleets:
            fleet.tick(delta_time, self)

    def begin_interactions(self):
        for flyer in self.all_objects:
            flyer.begin_interactions(self)

    def end_interactions(self):
        for flyer in self.all_objects:
            flyer.end_interactions(self)

    def add_wavemaker(self, wavemaker):
        self.others.append(wavemaker)
