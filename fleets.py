# SpaceObjects
import u
from fleet import Fleet, ShipFleet, SaucerFleet, AsteroidFleet


class Fleets:
    def __init__(self, asteroids, missiles, saucers, saucer_missiles, ships):
        self.fleets = (AsteroidFleet(asteroids), Fleet(missiles), SaucerFleet(saucers), Fleet(saucer_missiles), ShipFleet(ships))

    @property
    def asteroids(self):
        return self.fleets[0]

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

    def clear(self):
        for fleet in self.fleets:
            fleet.clear()

    def draw(self, screen):
        for fleet in self.fleets:
            fleet.draw(screen)

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
        all_true = True
        for fleet in self.fleets:
            if not fleet.tick(delta_time, self):
                all_true = False
        return all_true

