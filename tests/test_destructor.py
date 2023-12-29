from core.fleets import Fleets
from invaders.destructor import Destructor
from invaders.invader_player import InvaderPlayer
from invaders.reserveplayer import ReservePlayer
from invaders.robotplayer import RobotPlayer
from tests.tools import FI


class TestDestructor:
    def test_destructor_exits(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(destructor := Destructor())
        assert fi.destructors
        destructor.end_interactions(fleets)
        assert not fi.destructors

    def test_destructor_scares_right_things_away(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(InvaderPlayer())
        fleets.append(ReservePlayer(1))
        fleets.append(RobotPlayer())
        assert fi.invader_players
        assert fi.robots
        assert fi.reserve_players
        fleets.append(destructor := Destructor())
        fleets.perform_interactions()
        assert not fi.invader_players
        assert not fi.robots
        assert not fi.reserve_players

    def test_player_explodes(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(InvaderPlayer())
        fleets.append(destructor := Destructor())
        fleets.perform_interactions()
        assert not fi.invader_players
        assert fi.invader_explosions

    def test_robot_explodes(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(RobotPlayer())
        fleets.append(destructor := Destructor())
        fleets.perform_interactions()
        assert not fi.robots
        assert fi.invader_explosions
