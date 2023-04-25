# test_saucer
from math import sin, pi

from pygame import Vector2

import u
from missile import Missile
from saucer import Saucer


class TestSaucer:
    def test_ready(self):
        saucer = Saucer()
        saucer.ready()
        assert saucer.position.x == 0
        assert saucer.velocity == u.SAUCER_VELOCITY
        assert saucer.zig_timer == u.SAUCER_ZIG_TIME
        assert saucer.missile_timer == u.SAUCER_MISSILE_DELAY
        saucer.zig_timer = 0
        saucer.missile_timer = 0
        saucer.ready()
        assert saucer.position.x == u.SCREEN_SIZE
        assert saucer.velocity == -u.SAUCER_VELOCITY
        assert saucer.zig_timer == u.SAUCER_ZIG_TIME
        assert saucer.missile_timer == u.SAUCER_MISSILE_DELAY

    def test_move(self):
        saucer = Saucer()
        saucer.ready()
        starting = saucer.position
        saucer.move(0.1, [], [], [])
        assert saucer.position.x == u.SAUCER_VELOCITY.x*0.1
        saucer.move(0.1, [], [], [])
        assert saucer.position.x == 2*u.SAUCER_VELOCITY.x*0.1

    def test_vanish_at_edge(self):
        saucer = Saucer()
        saucers = [saucer]
        saucer.ready()
        saucer.move(1, saucers, [], [])
        assert saucers
        while saucer.position.x < u.SCREEN_SIZE:
            assert saucers
            saucer.move(0.1, saucers, [], [])
        assert not saucers

    def test_right_to_left(self):
        saucer = Saucer()
        saucer.ready()
        saucer.ready()
        assert saucer.position.x == u.SCREEN_SIZE

    def test_can_only_fire_two(self):
        saucer = Saucer()
        saucer_missiles = []
        assert saucer.missile_timer == u.SAUCER_MISSILE_DELAY
        saucer.fire_if_possible(0.1, saucer_missiles, [])
        assert not saucer_missiles
        saucer.fire_if_possible(u.SAUCER_MISSILE_DELAY, saucer_missiles, [])
        assert len(saucer_missiles) == 1
        assert saucer.missile_timer == u.SAUCER_MISSILE_DELAY
        saucer.fire_if_possible(u.SAUCER_MISSILE_DELAY, saucer_missiles, [])
        assert len(saucer_missiles) == 2
        saucer.fire_if_possible(u.SAUCER_MISSILE_DELAY, saucer_missiles, [])
        assert len(saucer_missiles) == 2

    def test_random_missile_velocity_0(self):
        saucer = Saucer()
        saucer.velocity = Vector2(100, 200)
        zero_angle_velocity = Vector2(u.MISSILE_SPEED, 0)
        missile = saucer.missile_at_angle(0, saucer.velocity)
        assert missile.velocity == saucer.velocity + zero_angle_velocity

    def test_random_missile_velocity_90(self):
        saucer = Saucer()
        saucer.velocity = Vector2(100, 200)
        zero_angle_velocity = Vector2(u.MISSILE_SPEED, 0)
        missile = saucer.missile_at_angle(90, saucer.velocity)
        assert missile.velocity == saucer.velocity + zero_angle_velocity.rotate(90)

    def test_random_missile_position_90(self):
        saucer = Saucer()
        saucer.position = Vector2(123, 456)
        missile = saucer.missile_at_angle(90, saucer.velocity)
        expected_offset = Vector2(2*saucer.radius, 0).rotate(90)
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
        ship_missile = Missile.from_ship(p,v)
        assert ship_missile.score_list == u.MISSILE_SCORE_LIST
        saucer_missile = Missile.from_saucer(p,v)
        assert saucer_missile.score_list == [0, 0, 0]


