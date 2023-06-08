from pygame import Vector2

import u
from fleets import Fleets
from gunner import Gunner
from test_interactions import FI


class TestGunner:
    def test_exists(self):
        assert Gunner()

    def test_no_fire(self):
        delta_time = 0.1
        saucer_position = Vector2(0, 0 )
        ship_position = Vector2(1, 1)
        fleets = Fleets()
        Gunner().fire(delta_time, saucer_position, ship_position, fleets)
        assert not FI(fleets).saucer_missiles

    def test_fire(self):
        delta_time = u.SAUCER_MISSILE_DELAY
        saucer_position = Vector2(0, 0 )
        ship_position = Vector2(1, 1)
        fleets = Fleets()
        Gunner().fire(delta_time, saucer_position, ship_position, fleets)
        assert FI(fleets).saucer_missiles
