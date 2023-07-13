

class AsteroidAnalyzer:
    def __init__(self, shipmaker):
        self._shipmaker = shipmaker

    def is_safe(self, asteroid):
        return self._shipmaker.asteroid_is_safe(asteroid)