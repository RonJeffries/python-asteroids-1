
import pygame
import pytest
from pygame.math import clamp, Vector2

from mover import Mover
from ship import Ship


class TestAsteroids:
    def test_something(self):
        assert True == True

    def test_map_lambda(self):
        points = [Vector2(-3.0, -2.0), Vector2(-3.0, 2.0), Vector2(-5.0, 4.0),
                  Vector2(7.0, 0.0), Vector2(-5.0, -4.0), Vector2(-3.0, -2.0)]
        new_points = map(lambda pt: pt + Vector2(7, 4), points)
        for point in new_points:
            assert point.x >= 0
            assert point.x <= 14
            assert point.y >= 0
            assert point.y <= 9

    def test_map_comprehension(self):
        points = [Vector2(-3.0, -2.0), Vector2(-3.0, 2.0), Vector2(-5.0, 4.0),
                  Vector2(7.0, 0.0), Vector2(-5.0, -4.0), Vector2(-3.0, -2.0)]
        new_points = [point + Vector2(7, 4) for point in points]
        for point in new_points:
            assert point.x >= 0
            assert point.x <= 14
            assert point.y >= 0
            assert point.y <= 9

    def test_ship_move(self):
        ship = Ship(Vector2(50, 60))
        ship.mover.velocity = Vector2(10, 16)
        ship.mover.move(0.5)
        assert ship.mover.position == Vector2(55, 68)

    def test_ship_acceleration(self):
        ship = Ship(Vector2(0, 0))
        ship.angle = 45
        ship.acceleration = pygame.Vector2(100, 0)
        ship.power_on(0.5)
        assert ship.mover.velocity.x == pytest.approx(35.3553, 0.01)
        assert ship.mover.velocity.y == pytest.approx(-35.3553, 0.01)

    def test_mod(self):
        assert 1005 % 1000 == 5
        assert -5 % 1000 == 995

    def test_args(self):
        def local_function(a, b):
            return 10*a + b
        result = local_function(b=5, a=6)
        assert result == 65

    def test_clamp(self):
        zero = clamp(-1, 0, 3)
        assert zero == 0
        three = clamp(4, 0, 3)
        assert three == 3

    def test_mover(self):
        pos = Vector2(100, 200)
        vel = Vector2(10, 20)
        mover = Mover(pos, vel)
        mover.move(0.5)
        assert mover.position == Vector2(105, 210)





