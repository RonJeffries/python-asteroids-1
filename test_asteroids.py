
import pygame
import pytest

from ship import Ship

vector2 = pygame.Vector2


class TestAsteroids():
    def test_something(self):
        assert True == True

    def test_map_lambda(self):
        points = [vector2(-3.0, -2.0), vector2(-3.0, 2.0), vector2(-5.0, 4.0),
                  vector2(7.0, 0.0), vector2(-5.0, -4.0), vector2(-3.0, -2.0)]
        new_points = map(lambda pt: pt + vector2(7, 4), points)
        for point in new_points:
            assert point.x >= 0
            assert point.x <= 14
            assert point.y >= 0
            assert point.y <= 9

    def test_map_comprehension(self):
        points = [vector2(-3.0, -2.0), vector2(-3.0, 2.0), vector2(-5.0, 4.0),
                  vector2(7.0, 0.0), vector2(-5.0, -4.0), vector2(-3.0, -2.0)]
        new_points = [point + vector2(7, 4) for point in points]
        for point in new_points:
            assert point.x >= 0
            assert point.x <= 14
            assert point.y >= 0
            assert point.y <= 9

    def test_ship_move(self):
        ship = Ship(vector2(50, 60))
        ship.velocity = vector2(10, 16)
        ship.move(0.5)
        assert ship.position == vector2(55, 68)

    def test_ship_acceleration(self):
        ship = Ship(vector2(0, 0))
        ship.angle = 45
        ship.acceleration = pygame.Vector2(100, 0)
        ship.power_on(0.5)
        assert ship.velocity.x == pytest.approx(35.3553, 0.01)
        assert ship.velocity.y == pytest.approx(-35.3553, 0.01)

    def test_mod(self):
        assert 1005 % 1000 == 5
        assert -5 % 1000 == 995


