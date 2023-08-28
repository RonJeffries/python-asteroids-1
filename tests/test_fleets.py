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


class Remindable:
    def __init__(self):
        self.reminded = False
        self.value = 37
        self.compared = False

    def set_true(self):
        self.reminded = True

    def set_value(self, value=42):
        self.value = value

    def compare(self, a, b):
        self.compared = a == b

    def begin_interactions(self, fleets):
        pass

    def end_interactions(self, fleets):
        pass

    def interact_with(self, other, fleets):
        fleets.remind_me(self, self.compare, 96, 96)


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

    def test_reminders(self):
        fleets = Fleets()
        obj = Remindable()
        fleets.remind_me(obj, obj.set_true)
        assert not obj.reminded
        fleets.execute_reminders(obj)
        assert obj.reminded

    def test_two_reminders(self):
        fleets = Fleets()
        obj = Remindable()
        fleets.remind_me(obj, obj.set_true)
        fleets.remind_me(obj, obj.set_value)
        assert not obj.reminded
        assert obj.value == 37
        fleets.execute_reminders(obj)
        assert obj.reminded
        assert obj.value == 42

    def test_parameters(self):
        fleets = Fleets()
        obj = Remindable()
        fleets.remind_me(obj, obj.compare, 666, 333+333)
        assert obj.value == 37
        fleets.execute_reminders(obj)
        assert obj.compared

    def test_reminder_form(self):
        obj = Remindable()
        reminder = [obj.set_value, 666]
        func = reminder[0]
        arg = reminder[1]
        func(arg)
        assert obj.value == 666

    def test_two_parameters(self):
        obj = Remindable()
        assert not obj.compared
        reminder = [obj.compare, [666, 333+333]]
        func = reminder[0]
        args = reminder[1]
        func(*args)
        assert obj.compared

    def test_fleets_interaction_cycle(self):
        obj = Remindable()
        fleets = Fleets()
        fleets. append(obj)
        fleets.append(Remindable())
        fleets.begin_interactions()
        fleets.perform_interactions()
        fleets.end_interactions()
        assert obj.compared





