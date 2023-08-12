from fleets import Fleets
from invader_player import InvaderPlayer
from tests.tools import FI


class TestPlayer:
    def test_left_edge(self):
        player = InvaderPlayer()
        player.move(-10000)
        assert player.rect.centerx == player.left

    def test_right_edge(self):
        player = InvaderPlayer()
        player.move(10000)
        assert player.rect.centerx == player.right

    def test_can_fire_initially(self):
        fleets = Fleets()
        fi = FI(fleets)
        player = InvaderPlayer()
        fleets.append(player)
        player.attempt_firing(fleets)
        assert fi.player_shots
