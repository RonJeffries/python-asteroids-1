import pytest
from pygame import Vector2

import u
from fleets import Fleets
from gunner import Gunner
from saucer import Saucer
from ship import Ship
from test_interactions import FI


class TestGunner:
    def test_exists(self):
        assert Gunner()

    def test_no_fire_on_short_time(self):
        delta_time = 0.1
        ship_position = Vector2(1, 1)
        ship = Ship(ship_position)
        fleets = Fleets()
        Gunner().fire(delta_time, Saucer(), ship, fleets)
        assert not FI(fleets).missiles

    def test_fire_on_time(self):
        delta_time = u.SAUCER_MISSILE_DELAY
        ship_position = Vector2(1, 1)
        ship = Ship(ship_position)
        fleets = Fleets()
        Gunner().fire(delta_time, Saucer(), ship, fleets)
        assert FI(fleets).missiles

    # def test_random_missile(self):
    #     no_target = 0.5
    #     angle = 0.0
    #     fleets = Fleets()
    #     fi = FI(fleets)
    #     position = Vector2(500, 500)
    #     Gunner().create_random_missile(angle, position, Vector2(12, 34), fleets)
    #     assert fi.saucer_missiles
    #     missile = fi.saucer_missiles[0]
    #     assert missile.position == position + Vector2(40, 0)
    #     assert missile.velocity_testing_only == Vector2(u.MISSILE_SPEED + 12, 34)

    def test_can_only_fire_limited_number(self):
        no_target = 0.5
        angle = 0.0
        fleets = Fleets()
        fi = FI(fleets)
        saucer_position = Vector2(500, 500)
        velocity = Vector2(0, 0)
        ship_position = Vector2(0, 0)
        saucer = Saucer()
        saucer._location.position = saucer_position
        saucer._location.velocity = velocity
        saucer.missile_tally = u.SAUCER_MISSILE_LIMIT
        Gunner().fire_missile(saucer, ship_position, fleets)
        assert not fi.missiles

    def test_targeted(self):
        fleets = Fleets()
        fi = FI(fleets)
        saucer_position = Vector2(500, 500)
        ship_position = Vector2(500, 550)
        Gunner().create_targeted_missile(saucer_position, ship_position, Vector2(0, 0), fleets)
        missile = fi.missiles[0]
        assert missile.velocity_testing_only.x == 0
        assert missile.velocity_testing_only.y == u.MISSILE_SPEED

    def test_targeted_harder(self):
        fleets = Fleets()
        fi = FI(fleets)
        saucer_position = Vector2(500, 500)
        ship_position = Vector2(550, 550)
        Gunner().create_targeted_missile(saucer_position, ship_position, Vector2(0, 0), fleets)
        missile = fi.missiles[0]
        assert missile.velocity_testing_only.x == pytest.approx(missile.velocity_testing_only.y)
        assert missile.velocity_testing_only.y == pytest.approx(u.MISSILE_SPEED*0.707, 0.1)

    def test_handle_ship_none(self):
        delta_time = 1.0
        tally = 0
        fleets = Fleets()
        fi = FI(fleets)
        ship = None
        Gunner().fire(delta_time, Saucer(), ship, fleets)
        assert fi.missiles



