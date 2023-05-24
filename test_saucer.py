# test_saucer

import pytest
from pygame import Vector2

import u
from fleet import MissileFleet
from missile import Missile
from saucer import Saucer
from ship import Ship


class TestSaucer:
    def test_alternating_direction(self):
        Saucer.init_for_new_game()
        saucer = Saucer()
        assert saucer.position.x == 0
        assert saucer.velocity_testing_only == u.SAUCER_VELOCITY
        assert saucer.missile_timer.elapsed == 0
        saucer.missile_timer.elapsed = 0.5
        saucer = Saucer()
        assert saucer.position.x == u.SCREEN_SIZE
        assert saucer.velocity_testing_only == -u.SAUCER_VELOCITY
        assert saucer.zig_timer.delay == u.SAUCER_ZIG_TIME
        assert saucer.zig_timer.elapsed == 0
        assert saucer.missile_timer.elapsed == 0

    def test_move(self):
        Saucer.init_for_new_game()
        saucer = Saucer()
        saucer.ready()
        saucer.move(delta_time=0.1, saucers=[])
        assert saucer.position.x == u.SAUCER_VELOCITY.x * 0.1
        saucer.move(delta_time=0.1, saucers=[])
        assert saucer.position.x == 2 * u.SAUCER_VELOCITY.x * 0.1

    def test_vanish_at_edge(self):
        Saucer.init_for_new_game()
        saucer = Saucer()
        saucers = [saucer]
        assert saucer.position.x == 0
        saucer.move(1, saucers)
        assert saucers
        time = 0
        delta_time = 0.1
        while time < 10:
            time += delta_time
            saucer.move(delta_time=delta_time, saucers=saucers)
        assert not saucers

    def test_right_to_left(self):
        Saucer.init_for_new_game()
        _saucer = Saucer()
        saucer = Saucer()
        assert saucer.position.x == u.SCREEN_SIZE

    def test_off_low(self):
        saucer = Saucer()
        saucer.move_to(Vector2(100, 3))
        saucer.accelerate_to(Vector2(100, -100))
        saucer.move(0.1, [])
        assert saucer.position.y > 1000

    def test_off_high(self):
        saucer = Saucer()
        saucer.move_to(Vector2(100, 1021))
        saucer.accelerate_to(Vector2(100, 100))
        saucer.move(0.1, [])
        assert saucer.position.y < 50

    def test_can_only_fire_two(self):
        saucer = Saucer()
        saucer_missiles = MissileFleet([], u.SAUCER_MISSILE_LIMIT)
        saucer.fire_if_possible(delta_time=0.1, saucer_missiles=saucer_missiles, ships=[])
        assert not saucer_missiles
        saucer.fire_if_possible(u.SAUCER_MISSILE_DELAY, saucer_missiles=saucer_missiles, ships=[])
        assert len(saucer_missiles) == 1
        saucer.fire_if_possible(u.SAUCER_MISSILE_DELAY, saucer_missiles=saucer_missiles, ships=[])
        assert len(saucer_missiles) == 2
        saucer.fire_if_possible(u.SAUCER_MISSILE_DELAY, saucer_missiles=saucer_missiles, ships=[])
        assert len(saucer_missiles) == 2

    def test_random_missile_velocity_0(self):
        saucer = Saucer()
        saucer.accelerate_to(Vector2(100, 200))
        zero_angle_velocity = Vector2(u.MISSILE_SPEED, 0)
        missile = saucer.missile_at_angle(0, saucer.velocity_testing_only)
        assert missile.velocity_testing_only == saucer.velocity_testing_only + zero_angle_velocity

    def test_random_missile_velocity_90(self):
        saucer = Saucer()
        saucer.accelerate_to(Vector2(100, 200))
        zero_angle_velocity = Vector2(u.MISSILE_SPEED, 0)
        missile = saucer.missile_at_angle(90, saucer.velocity_testing_only)
        assert missile.velocity_testing_only == saucer.velocity_testing_only + zero_angle_velocity.rotate(90)

    def test_random_missile_position_90(self):
        saucer = Saucer()
        saucer.move_to(Vector2(123, 456))
        missile = saucer.missile_at_angle(90, saucer.velocity_testing_only)
        expected_offset = Vector2(2 * saucer.radius, 0).rotate(90)
        assert missile.position == saucer.position + expected_offset

    def test_vectors_mutate(self):
        v1 = Vector2(1, 2)
        v1_original = v1
        assert v1 is v1_original
        v2 = Vector2(3, 4)
        v1 += v2
        assert v1 is v1_original
        v1 = v1 + v2
        assert v1 is not v1_original

    def test_missile_scoring(self):
        p = Vector2(12, 34)
        v = Vector2(56, 78)
        ship_missile = Missile.from_ship(p, v)
        assert ship_missile.score_list == u.MISSILE_SCORE_LIST
        saucer_missile = Missile.from_saucer(p, v)
        assert saucer_missile.score_list == [0, 0, 0]

    def test_missile_spec_targeted(self):
        saucer = Saucer()
        saucer.move_to(Vector2(100, 110))
        saucer.accelerate_to(Vector2(99, 77))
        ships = [Ship(Vector2(100, 100))]
        should_target = 0.1
        random_angle = None
        missile = saucer.suitable_missile(should_target, random_angle, ships)
        assert missile.velocity_testing_only == Vector2(0, -u.SPEED_OF_LIGHT / 3)
        # assert degrees == -90

    def test_missile_spec_no_ship(self):
        saucer = Saucer(Vector2(100, 110))
        saucer.accelerate_to(Vector2(99, 77))
        ships = []
        should_target = 0.1
        random_angle = 0.5
        missile = saucer.suitable_missile(should_target, random_angle, ships)
        assert missile.velocity_testing_only.x - saucer.velocity_testing_only.x == pytest.approx(-166.667, 0.01)

    def test_missile_spec_no_dice(self):
        saucer = Saucer(Vector2(100, 110))
        saucer.accelerate_to(Vector2(99, 77))
        ships = [Ship(Vector2(100, 100))]
        should_target = 0.26
        random_angle = 0.5
        missile = saucer.suitable_missile(should_target, random_angle, ships)
        assert missile.velocity_testing_only.x == pytest.approx(-67.666, 0.01)
        assert missile.velocity_testing_only.y == 77

    def test_empty_string(self):
        assert not ""
        assert "False"

    def test_methods(self):
        methods = dir(Saucer)
        methods = [x for x in methods if callable(getattr(Saucer, x))]
        methods = [x for x in methods if not x.startswith("__")]
        for m in methods:
            print(m)
        assert True
