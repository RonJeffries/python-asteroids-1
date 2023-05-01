# SpaceObjects

class Fleets:
    def __init__(self, asteroids, missiles, saucers, saucer_missiles, ships):
        self.fleets = (asteroids, missiles, saucers, saucer_missiles, ships)

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
            for flyer in fleet:
                flyer.draw(screen)

