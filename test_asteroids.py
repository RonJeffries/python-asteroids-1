
import pygame
import pytest
from pygame.math import clamp, Vector2

import u
from game import next_wave_size, Game
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
        ship.velocity = Vector2(10, 16)
        ship.move(0.5)
        assert ship.position == Vector2(55, 68)

    def test_ship_acceleration(self):
        ship = Ship(Vector2(0, 0))
        ship.angle = 45
        ship.acceleration = pygame.Vector2(100, 0)
        ship.power_on(0.5)
        assert ship.velocity.x == pytest.approx(35.3553, 0.01)
        assert ship.velocity.y == pytest.approx(-35.3553, 0.01)

    def test_mod(self):
        assert 1005 % 1000 == 5
        assert -5 % 1000 == 995

    def test_slice(self):
        score = "0000200"
        slice = score[-5:]
        assert slice == "00200"

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
        things = [1,2,3,4]
        assert things.pop() == 4

    def test_missile_start(self):
        ship = Ship(Vector2(100, 100))
        ship.angle = 45
        pos = ship.missile_start()
        assert pos.x == pytest.approx(100+25, 0.5)
        assert pos.y == pytest.approx(100-25, 0.5)

    def test_missile_velocity(self):
        ship = Ship(Vector2(100, 100))
        ship.angle = 45
        ship.velocity = Vector2(500, 500)
        velocity = ship.missile_velocity()
        own_velocity = Vector2(u.MISSILE_SPEED, 0).rotate(-45)
        total_velocity = own_velocity + Vector2(500, 500)
        assert velocity == total_velocity

    def test_missile_timeout(self):
        ship = Ship(Vector2(100,100))
        missiles = []
        ship.fire_if_possible(missiles)
        assert len(missiles) == 1
        missile = missiles[0]
        missile.update(missiles, 0.5)
        assert len(missiles) == 1
        missile.update(missiles, 3.0)
        assert len(missiles) == 0

    def test_wave_sizes(self):
        game = Game(True)
        game.asteroids_in_this_wave = 2
        game.set_instance(game)
        assert next_wave_size() == 4
        assert next_wave_size() == 6
        assert next_wave_size() == 8
        assert next_wave_size() == 10
        assert next_wave_size() == 11
        assert next_wave_size() == 11
        # game_init()






