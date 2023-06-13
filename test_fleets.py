from pygame import Vector2

from fleets import Fleets
from missile import Missile
from test_interactions import FI


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
        saucer_missiles = []
        fleets = Fleets([], [], [], saucer_missiles, [])
        fi = FI(fleets)
        assert len(fi.saucer_missiles) == 0
        fleets.add_flyer(Missile.from_saucer(Vector2(0, 0), Vector2(0, 0)))
        fleets.add_flyer(Missile.from_saucer(Vector2(0, 0), Vector2(20, 20)))
        fleets.add_flyer(Missile.from_saucer(Vector2(0, 0), Vector2(30, 30)))
        assert len(fi.saucer_missiles) == 3
        assert fi.saucer_missiles[1]._location.velocity.x == 20

    def test_copies_all_objects(self):
        fleets = Fleets()
        assert fleets.all_objects is not fleets.flyers


