# SpaceObjects

from fleet import Fleet, ShipFleet


class Fleets:
    def __init__(self, asteroids, missiles, saucers, saucer_missiles, ships):
        self.fleets = (Fleet(asteroids), Fleet(missiles), Fleet(saucers), Fleet(saucer_missiles), ShipFleet(ships))

    @property
    def asteroids(self):
        return self.fleets[0].flyers

    @property
    def missiles(self):
        return self.fleets[1].flyers

    @property
    def saucers(self):
        return self.fleets[2].flyers

    @property
    def saucer_missiles(self):
        return self.fleets[3].flyers

    @property
    def ships(self):
        return self.fleets[4].flyers

    def draw(self, screen):
        for fleet in self.fleets:
            fleet.draw(screen)

    def tick(self, delta_time):
        result = True
        for fleet in self.fleets:
            result = result and fleet.tick(delta_time, self)
        return result

