# SpaceObjects

class SpaceObjects:
    def __init__(self, asteroids, missiles, saucers, saucer_missiles, ships):
        self.asteroids = asteroids
        self.missiles = missiles
        self.saucers = saucers
        self.saucer_missiles = saucer_missiles
        self.ships = ships
        self.collections = (asteroids, missiles, saucers, saucer_missiles, ships)

