from core.fleets import Fleets
from invaders.invaders_saucer_maker import InvadersSaucerMaker
from tests.tools import FI


class FakeInvaderFleet:
    def __init__(self, invaders):
        self.invaders = invaders

    def invader_count(self):
        return self.invaders


class FakeInvaderPlayer:
    def __init__(self, shot_count):
        self.shot_count = shot_count


class TestInvadersSaucerMaker:

    def test_exists(self):
        maker = InvadersSaucerMaker()

    def test_happy_path(self):
        fleets = Fleets()
        fi = FI(fleets)
        invader_fleet = FakeInvaderFleet(8)
        invader_player = FakeInvaderPlayer(0)
        maker = InvadersSaucerMaker()
        maker.begin_interactions(fleets)
        maker.interact_with_invaderfleet(invader_fleet, fleets)
        maker.interact_with_invaderplayer(invader_player, fleets)
        maker.end_interactions(fleets)
        assert len(fi.time_capsules) == 1
        assert len(fi.invader_saucers) == 1

    def test_no_player(self):
        fleets = Fleets()
        fi = FI(fleets)
        invader_fleet = FakeInvaderFleet(8)
        maker = InvadersSaucerMaker()
        maker.begin_interactions(fleets)
        maker.interact_with_invaderfleet(invader_fleet, fleets)
        maker.end_interactions(fleets)
        assert len(fi.time_capsules) == 1
        assert len(fi.invader_saucers) == 0

    def test_too_few_invaders(self):
        fleets = Fleets()
        fi = FI(fleets)
        invader_fleet = FakeInvaderFleet(7)
        invader_player = FakeInvaderPlayer(0)
        maker = InvadersSaucerMaker()
        maker.begin_interactions(fleets)
        maker.interact_with_invaderfleet(invader_fleet, fleets)
        maker.interact_with_invaderplayer(invader_player, fleets)
        maker.end_interactions(fleets)
        assert len(fi.time_capsules) == 1
        assert len(fi.invader_saucers) == 0
