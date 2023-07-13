import u


class AsteroidAnalyzer:
    def __init__(self, shipmaker):
        self._shipmaker = shipmaker

    def is_safe(self, asteroid):
        return self.asteroid_is_safe(asteroid)

    def asteroid_is_safe(self, asteroid):
        safe = True
        distance = asteroid.position.distance_to(u.CENTER)
        ship_radius = 25
        if distance < ship_radius + asteroid.radius:
            safe = False
        elif distance < u.SAFE_EMERGENCE_DISTANCE:
            ml = asteroid._location
            if not ml.moving_away_from(u.CENTER):
                safe = False
        return safe
