import pytest
from pygame import Vector2

from fleets import Fleets
from missile import Missile
from tests.tools import FI


class FakeFlyer:
    def __init__(self):
        pass

    def control_motion(self, delta_time):
        pass

    def fire_if_possible(self, _delta_time, _saucer_missiles, _ships):
        pass

    def move(self, delta_time, fleet):
        pass

    @staticmethod
    def tick(_delta_time, _fleet, _fleets):
        pass


class TestFleets:
    def test_len_etc(self):
        fleets = Fleets()
        fi = FI(fleets)
        assert len(fi.missiles) == 0
        fleets.append(Missile("saucer", Vector2(0, 0), Vector2(0, 0)))
        fleets.append(Missile("saucer", Vector2(0, 0), Vector2(20, 20)))
        fleets.append(Missile("saucer", Vector2(0, 0), Vector2(30, 30)))
        assert len(fi.missiles) == 3
        assert fi.missiles[1]._location.velocity.x == 20

    def test_copies_all_objects(self):
        fleets = Fleets()
        assert fleets.all_objects is not fleets.flyers

    def test_empty_list(self):
        a = []
        b = []
        a.append("x")
        assert "x" in a
        assert "x" not in b





