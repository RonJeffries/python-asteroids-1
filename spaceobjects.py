# SpaceObjects

class SpaceObjects:
    def __init__(self, asteroids, missiles, saucers, saucer_missiles, ships):
        self.collections = (asteroids, missiles, saucers, saucer_missiles, ships)

    @property
    def asteroids(self):
        return self.collections[0]

    @property
    def missiles(self):
        return self.collections[1]

    @property
    def saucers(self):
        return self.collections[2]

    @property
    def saucer_missiles(self):
        return self.collections[3]

    @property
    def ships(self):
        return self.collections[4]

