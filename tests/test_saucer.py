# test_saucer
from math import degrees

import pytest
from pygame import Vector2

import u
from fleets import Fleets
from missile import Missile
from saucer import Saucer
from saucermaker import SaucerMaker
from scorekeeper import ScoreKeeper
from ship import Ship
from test_interactions import FI


class TestSaucer:
    def test_alternating_direction(self):
        Saucer.init_for_new_game()
        saucer = Saucer.large()
        assert saucer.position.x == 0
        assert saucer.velocity == u.SAUCER_VELOCITY
        saucer = Saucer.large()
        assert saucer.position.x == u.SCREEN_SIZE
        assert saucer.velocity == -u.SAUCER_VELOCITY
        assert saucer._zig_timer.delay == u.SAUCER_ZIG_TIME
        assert saucer._zig_timer.elapsed == 0

    def test_move(self):
        Saucer.init_for_new_game()
        saucer = Saucer.large()
        saucer._move(delta_time=0.1, fleets=[])
        assert saucer.position.x == u.SAUCER_VELOCITY.x * 0.1
        saucer._move(delta_time=0.1, fleets=[])
        assert saucer.position.x == 2 * u.SAUCER_VELOCITY.x * 0.1

    def test_vanish_at_edge(self):
        Saucer.init_for_new_game()
        fleets = Fleets()
        fi = FI(fleets)
        saucer = Saucer.large()
        fleets.append(saucer)
        assert saucer.position.x == 0
        saucer.update(1, fleets)
        assert fi.saucers
        time = 0
        delta_time = 0.1
        while time < 10:
            time += delta_time
            saucer.update(delta_time=delta_time, fleets=fleets)
        assert not fi.saucers

    def test_right_to_left(self):
        Saucer.init_for_new_game()
        _saucer = Saucer.large()
        saucer = Saucer.large()
        assert saucer.position.x == u.SCREEN_SIZE

    def test_off_low(self):
        saucer = Saucer.large()
        saucer.move_to(Vector2(100, 3))
        saucer.accelerate_to(Vector2(100, -100))
        saucer._move(0.1, [])
        assert saucer.position.y > 1000

    def test_off_high(self):
        saucer = Saucer.large()
        saucer.move_to(Vector2(100, 1021))
        saucer.accelerate_to(Vector2(100, 100))
        saucer._move(0.1, [])
        assert saucer.position.y < 50

    def test_can_only_fire_two(self):
        fleets = Fleets()
        fi = FI(fleets)
        saucer = Saucer.large()
        ship_missile = Missile.from_ship("ship", Vector2(0, 0), Vector2(0, 0))
        saucer.fire_if_possible(delta_time=0.1, fleets=fleets)
        assert not fi.missiles
        fleets.append(ship_missile)  # add extra ship missile
        extra = 1
        saucer.fire_if_possible(u.SAUCER_MISSILE_DELAY, fleets=fleets)
        assert len(fi.missiles) == 1 + extra
        saucer.begin_interactions(fleets)
        for m in fi.missiles:
            saucer.interact_with_missile(m, fleets)
        saucer.fire_if_possible(u.SAUCER_MISSILE_DELAY, fleets=fleets)
        assert len(fi.missiles) == 2 + extra
        saucer.begin_interactions(fleets)
        for m in fi.missiles:
            saucer.interact_with_missile(m, fleets)
        saucer.fire_if_possible(u.SAUCER_MISSILE_DELAY, fleets=fleets)
        assert len(fi.missiles) == 2 + extra

    def test_counts_only_saucer_missiles(self):
        fleets = Fleets()
        saucer = Saucer.large()
        assert saucer.missile_tally == 0
        saucer.missile_tally = 5
        saucer.begin_interactions(fleets)
        assert saucer.missile_tally == 0
        saucer_missile = Missile.from_saucer("saucer", saucer.position, Vector2(0, 0))
        saucer.interact_with_missile(saucer_missile, fleets)
        assert saucer.missile_tally == 1
        ship_missile = Missile.from_ship("ship", saucer.position, Vector2(0, 0))
        saucer.interact_with_missile(ship_missile, fleets)
        assert saucer.missile_tally == 1

    def test_vectors_mutate(self):
        v1 = Vector2(1, 2)
        v1_original = v1
        assert v1 is v1_original
        v2 = Vector2(3, 4)
        v1 += v2
        assert v1 is v1_original
        v1 = v1 + v2
        assert v1 is not v1_original

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

    def test_saucer_sizing(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(keeper := ScoreKeeper())
        fleets.append(maker := SaucerMaker())
        fleets.perform_interactions()
        keeper.score = 0
        fleets.tick(u.SAUCER_EMERGENCE_TIME)
        saucers = fi.saucers
        assert saucers
        saucer = saucers[0]
        assert not saucer.is_small_saucer
        fleets.remove(saucer)
        keeper.score = u.SAUCER_SCORE_FOR_SMALL
        fleets.tick(u.SAUCER_EMERGENCE_TIME)
        saucers = fi.saucers
        assert saucers
        saucer = saucers[0]
        assert saucer.is_small_saucer




