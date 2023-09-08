from fleets import Fleets
from player_shot import PlayerShot
from tests.tools import FI
from timecapsule import TimeCapsule


class TestTimeCapsule:
    def test_can_create(self):
        thing = "thing"
        capsule = TimeCapsule(thing, 2)

    def test_after_a_while(self):
        crocodile = PlayerShot((100, 100))
        a_while = 2
        capsule = TimeCapsule(crocodile, a_while)
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(capsule)
        fleets.tick(1.1)
        assert not fi.player_shots
        fleets.tick(1)
        assert fi.player_shots
        assert fi.player_shots[0] == crocodile
