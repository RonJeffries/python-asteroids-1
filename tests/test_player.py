import u
from core.fleets import Fleets
from invaders.invader_player import InvaderPlayer
from invaders.player_explosion import PlayerExplosion
from tests.tools import FI, FakeFleets


class TestPlayer:
    def test_start_left(self):
        player = InvaderPlayer()
        assert player._sprite.centerx == u.INVADER_PLAYER_LEFT

    def test_left_edge(self):
        player = InvaderPlayer()
        player.move(-10000)
        assert player._sprite.centerx == u.INVADER_PLAYER_LEFT

    def test_right_edge(self):
        player = InvaderPlayer()
        player.move(10000)
        assert player._sprite.centerx == u.INVADER_PLAYER_RIGHT

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

    def test_collision_removes_self(self):
        fleets = FakeFleets()
        player = InvaderPlayer()
        player.explode(fleets)
        assert player in fleets.removes
        # added_tc = [tc for tc in fleets.appends if isinstance(tc, TimeCapsule)]
        # assert added_tc

    def test_firing_counts_shots(self):
        player = InvaderPlayer()
        assert player.shot_count == 0
        player.fire([])
        assert player.shot_count == 1
        player.fire([])
        assert player.shot_count == 2


class TestPlayerExplosion:
    def test_exists(self):
        PlayerExplosion((100, 200))

    def test_position(self):
        player_position = (100, 200)
        explosion = PlayerExplosion(player_position)
        assert explosion.position == player_position








