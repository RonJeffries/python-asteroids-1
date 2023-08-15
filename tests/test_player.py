import pygame

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

    def test_cannot_fire_with_one_on_screen(self):
        fleets = Fleets()
        fi = FI(fleets)
        player = InvaderPlayer()
        fleets.append(player)
        player.begin_interactions(fleets)
        player.attempt_firing(fleets)
        assert len(fi.player_shots) == 1
        shot = fi.player_shots[0]
        player.begin_interactions(fleets)
        player.interact_with_playershot(shot, fleets)
        player.attempt_firing(fleets)
        assert len(fi.player_shots) == 1

    def test_trigger_logic(self):
        fleets = Fleets()
        player = InvaderPlayer()
        assert player.fire_request_allowed
        player.trigger_pulled(fleets)
        assert not player.fire_request_allowed
        player.trigger_released()
        assert player.fire_request_allowed

    def test_firing_with_trigger(self):
        fleets = Fleets()
        fi = FI(fleets)
        player = InvaderPlayer()
        player.trigger_pulled(fleets)
        assert fi.player_shots
        fleets.clear()
        player.trigger_pulled(fleets)
        assert not fi.player_shots
        player.trigger_released()
        player.trigger_pulled(fleets)
        assert fi.player_shots





