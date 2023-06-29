import pytest
from pygame import Vector2

import u
from fleets import Fleets
from gunner import Gunner
from saucer import Saucer
from ship import Ship
from shot_optimizer import ShotOptimizer, TimeToTarget
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
        Gunner().fire_if_missile_available(saucer, ship_position, fleets)
        assert not fi.missiles

    def test_timer_reset(self):
        fleets = Fleets()
        fi = FI(fleets)
        saucer = Saucer()
        saucer.missile_tally = u.SAUCER_MISSILE_LIMIT
        gunner = Gunner()
        gunner.fire(u.SAUCER_MISSILE_DELAY,saucer, None, fleets)
        assert not fi.missiles
        saucer.missile_tally = 0
        gunner.fire(0.1, saucer, None, fleets)
        assert fi.missiles

    def test_targeted(self):
        fleets = Fleets()
        fi = FI(fleets)
        saucer_position = Vector2(500, 500)
        ship_position = Vector2(500, 550)
        Gunner().create_unoptimized_missile(saucer_position, ship_position, fleets)
        missile = fi.missiles[0]
        assert missile.velocity_testing_only.x == 0
        assert missile.velocity_testing_only.y == u.MISSILE_SPEED

    def test_targeted_harder(self):
        fleets = Fleets()
        fi = FI(fleets)
        saucer_position = Vector2(500, 500)
        ship_position = Vector2(550, 550)
        Gunner().create_unoptimized_missile(saucer_position, ship_position, fleets)
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

    def test_large_saucer_does_not_target(self):
        pos = Vector2(100, 100)
        fleets = Fleets()
        fi = FI(fleets)
        ship = Ship(Vector2(100, 100))
        large_saucer = Saucer(2)
        large_saucer._location.position = Vector2(100, 50)
        large_gunner = large_saucer._gunner
        large_gunner.fire_available_missile(0.26, fleets, large_saucer, ship)
        missiles = fi.missiles
        assert missiles
        missile = missiles[0]
        velocity = missile.velocity_testing_only
        assert velocity.x != 0 or velocity.y != pytest.approx(u.MISSILE_SPEED, .001)  # not straight up

    def test_small_saucer_does_target(self):
        pos = Vector2(100, 100)
        fleets = Fleets()
        fi = FI(fleets)
        ship = Ship(Vector2(100, 100))
        small_saucer = Saucer(1)
        small_saucer._location.position = Vector2(100, 50)
        small_gunner = small_saucer._gunner
        small_gunner.fire_available_missile(0, fleets, small_saucer, ship)
        missiles = fi.missiles
        assert missiles
        missile = missiles[0]
        velocity = missile.velocity_testing_only
        assert velocity.x == 0
        assert velocity.y != 0  # straight up

    def test_time_to_target_1(self):
        time = TimeToTarget(Vector2(0, 50), Vector2(0, 0)).time
        assert time == 50/u.MISSILE_SPEED

    def test_time_to_target_harder(self):
        time = TimeToTarget(Vector2(0, 50), Vector2(0, 10)).time
        missile_position = u.MISSILE_SPEED * time
        ship_distance = 10*time
        ship_position = 50 + ship_distance
        assert missile_position == pytest.approx(ship_position)

    def test_time_to_target_impossible(self):
        time = TimeToTarget(Vector2(0, 50), Vector2(0, u.MISSILE_SPEED)).time
        assert time == 0

    def test_time_to_target_long(self):
        time = TimeToTarget(Vector2(0, 50), Vector2(0, u.MISSILE_SPEED - 1)).time
        assert time == 50

    def test_hits_target(self):
        fleets = Fleets()
        fi = FI(fleets)
        gunner = Gunner(10)
        ship = Ship(Vector2(100, 100))
        ship._location.velocity = Vector2(37, 59)
        saucer = Saucer(1)
        saucer.move_to(Vector2(19, 43))
        relative_position = Vector2(100, 100) - Vector2(19, 43)
        relative_velocity = Vector2(37, 59)
        time = TimeToTarget(relative_position, relative_velocity).time
        assert time
        gunner.fire_if_missile_available(saucer, ship, fleets)
        assert fi.missiles
        missile = fi.missiles[0]
        missile_pos = missile.position + missile.velocity_testing_only*time
        ship_pos = ship.position + ship.velocity*time
        assert missile_pos.distance_to(ship_pos) == pytest.approx(0)







