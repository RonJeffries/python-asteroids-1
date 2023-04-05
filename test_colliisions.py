from pygame import Vector2

import u
from asteroid import Asteroid
from main import set_ship_timer, check_ship_spawn, safe_to_emerge
from missile import Missile
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

    def test_respawn_ship(self):
        ship = Ship(Vector2(0, 0))
        ship.velocity = Vector2(31, 32)
        ship.angle = 90
        ships = []
        set_ship_timer(3)
        check_ship_spawn(ship, ships, 0.1)
        assert not ships
        check_ship_spawn(ship, ships, u.SHIP_EMERGENCE_TIME)
        assert ships
        assert ship.position == u.CENTER
        assert ship.velocity == Vector2(0, 0)
        assert ship.angle == 0

    def test_safe_to_emerge_hates_missiles(self):
        missiles = []
        asteroids = []
        assert safe_to_emerge(missiles, asteroids)
        missiles.append(Missile(Vector2(0, 0), Vector2(0, 0)))
        assert not safe_to_emerge(missiles, asteroids)

    def test_safe_to_emerge_hates_close_asteroids(self):
        asteroids = []
        missiles = []
        assert safe_to_emerge(missiles, asteroids)
        asteroids.append(Asteroid(2, u.CENTER))
        assert not safe_to_emerge(missiles, asteroids)


