

class AsteroidAnalyzer:
    def __init__(self, shipmaker):
        self._shipmaker = shipmaker

    def is_safe(self, asteroid):
        return asteroid.is_safe_for_emergence()
