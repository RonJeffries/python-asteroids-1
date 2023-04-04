from pygame import Vector2

from asteroid import Asteroid
from ship import Ship


class TestCollisions:
    def test_far_away(self):
        ship = Ship(Vector2(0, 0))
        asteroid = Asteroid(2, Vector2(200,200))
        ship.collide_with_asteroid(asteroid)
        assert ship.active

    def test_close_enough(self):
        ship = Ship(Vector2(0, 0))
        asteroid = Asteroid(2, Vector2(50, 50))
        ship.collide_with_asteroid(asteroid)
        assert not ship.active
