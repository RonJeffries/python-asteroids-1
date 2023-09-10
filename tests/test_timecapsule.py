from fleets import Fleets
from invader_player import InvaderPlayer
from player_shot import PlayerShot
from reserveplayer import ReservePlayer
from tests.tools import FI
from timecapsule import TimeCapsule


class TestTimeCapsule:
    def test_can_create(self):
        thing = "thing"
        capsule = TimeCapsule(2, thing)

    def test_after_a_while(self):
        crocodile = PlayerShot((100, 100))
        a_while = 2
        capsule = TimeCapsule(a_while, crocodile)
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(capsule)
        fleets.tick(1.1)
        assert not fi.player_shots
        fleets.tick(1)
        assert fi.player_shots
        assert fi.player_shots[0] == crocodile

    def test_append_remove(self):
        reserve = ReservePlayer(2)
        player = InvaderPlayer()
        capsule = TimeCapsule(2, player, reserve)
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(reserve)
        fleets.append(capsule)
        assert fi.reserve_players
        assert not fi.invader_players
        fleets.tick(2.1)
        assert fi.invader_players
        assert not fi.reserve_players


