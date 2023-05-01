# SpaceObjects

from fleet import Fleet


class Fleets:
    def __init__(self, asteroids, missiles, saucers, saucer_missiles, ships):
        self.fleets = (Fleet(asteroids), Fleet(missiles), Fleet(saucers), Fleet(saucer_missiles), Fleet(ships))

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

    def move_everything(self, delta_time):
        for the_saucer in self.saucers.copy():
            the_saucer.move(delta_time, self.saucers, self.saucer_missiles, self.ships)
        for missile in self.saucer_missiles:
            missile.move(delta_time)
        for the_ship in self.ships:
            the_ship.move(delta_time)
        for asteroid in self.asteroids:
            asteroid.move(delta_time)
        for missile in self.missiles:
            missile.move(delta_time)

