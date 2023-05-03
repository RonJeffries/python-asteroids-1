# SpaceObjects

from fleet import Fleet, ShipFleet, SaucerFleet


class Fleets:
    def __init__(self, asteroids, missiles, saucers, saucer_missiles, ships):
        self.fleets = (Fleet(asteroids), Fleet(missiles), SaucerFleet(saucers), Fleet(saucer_missiles), ShipFleet(ships))

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

    def draw(self, screen):
        for fleet in self.fleets:
            fleet.draw(screen)

    def tick(self, delta_time):
        all_true = True
        for fleet in self.fleets:
            if not fleet.tick(delta_time, self):
                all_true = False
        return all_true

