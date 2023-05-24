
import pygame
import pytest
from pygame.math import clamp, Vector2

import u
from fleet import MissileFleet
from ship import Ship


class TestAsteroids:
    def test_something(self):
        assert True

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
        ship.velocity_testing_only = Vector2(10, 16)
        ship.move(0.5, [ship])
        assert ship.position == Vector2(55, 68)

    def test_ship_acceleration(self):
        ship = Ship(Vector2(0, 0))
        ship._angle = 45
        ship._acceleration = pygame.Vector2(100, 0)
        ship.power_on(0.5)
        assert ship.velocity_testing_only.x == pytest.approx(35.3553, 0.01)
        assert ship.velocity_testing_only.y == pytest.approx(-35.3553, 0.01)

    def test_mod(self):
        assert 1005 % 1000 == 5
        assert -5 % 1000 == 995

    def test_slice(self):
        score = "0000200"
        assert score[-5:] == "00200"

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

    def test_list_pop(self):
        things = [1, 2, 3, 4]
        assert things.pop() == 4

    def test_missile_start(self):
        ship = Ship(Vector2(100, 100))
        ship._angle = 45
        pos = ship.missile_start()
        assert pos.x == pytest.approx(100+25, 0.5)
        assert pos.y == pytest.approx(100-25, 0.5)

    def test_missile_velocity(self):
        ship = Ship(Vector2(100, 100))
        ship._angle = 45
        ship.velocity_testing_only = Vector2(500, 500)
        velocity = ship.missile_velocity()
        own_velocity = Vector2(u.MISSILE_SPEED, 0).rotate(-45)
        total_velocity = own_velocity + Vector2(500, 500)
        assert velocity == total_velocity

    def test_missile_timeout(self):
        ship = Ship(Vector2(100,100))
        missiles = MissileFleet([], 4)
        ship.fire_if_possible(missiles)
        assert len(missiles) == 1
        missile = missiles[0]
        missile.tick_timer(0.5, missiles)
        assert len(missiles) == 1
        missile.tick_timer(3.0, missiles)
        assert len(missiles) == 0

    def test_hyperspace(self):
        impossible = Vector2(-5, -5)
        impossible_angle = 370
        ship = Ship(impossible)
        ship._angle = impossible_angle
        ship.enter_hyperspace_if_possible([], 99, [])
        position = ship.position
        angle = ship._angle
        assert position != impossible and angle != impossible_angle
        assert ship._location.velocity != Vector2(0,0)
        ship.enter_hyperspace_if_possible([], 99, [])  # cannot fail
        assert ship.position == position and ship._angle == angle

    def test_hyperspace_failure(self):
        """hyperspace fails when random(0 thru 62) > asteroid count plus 44"""
        ship = Ship(u.CENTER)
        self.check_no_fail(ship, 0, 0)
        self.check_fail(ship, 45, 0)
        self.check_fail(ship, 62, 17)
        self.check_no_fail(ship, 62, 18)

    @staticmethod
    def check_no_fail(ship, roll, asteroids):
        assert not ship.hyperspace_failure(roll, asteroids)

    @staticmethod
    def check_fail(ship, roll, asteroids):
        assert ship.hyperspace_failure(roll, asteroids)








