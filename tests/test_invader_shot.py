import pytest
from pygame import Vector2

import u
from invaders.bitmap_maker import BitmapMaker
from core.fleets import Fleets
from invaders.invader_player import InvaderPlayer
from invaders.invader_shot import InvaderShot
from invaders.player_shot import PlayerShot
from invaders.roadfurniture import RoadFurniture
from invaders.sprite import Sprite
from tests.tools import FI


class TestInvaderShot:
    @pytest.fixture
    def shot(self):
        return InvaderShot(u.CENTER, Sprite.squiggles())

    def test_exists(self, shot):
        pass

    def test_moves_once_per_three_updates(self, shot):
        fleets = Fleets()
        assert shot.position == u.CENTER
        shot.update(1/60, fleets)
        assert shot.position == u.CENTER
        shot.update(1/60, fleets)
        assert shot.position == u.CENTER
        shot.update(1/60, fleets)
        assert shot.position == u.CENTER + Vector2(0, 16)

    def test_counts_moves(self, shot):
        fleets = Fleets()
        assert shot.moves == 0
        for _ in range(3):
            shot.update(1/60, fleets)
        assert shot.moves == 1
        for _ in range(3):
            shot.update(1/60, fleets)
        assert shot.moves == 2


    def test_dies_past_edge(self, shot):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(shot)
        current_pos = u.CENTER
        while current_pos.y < u.SCREEN_SIZE:
            assert shot.position == current_pos
            current_pos = current_pos + Vector2(0, 16)
            shot.update(1/60, fleets)
            shot.update(1/60, fleets)
            shot.update(1/60, fleets)
        assert shot.available
        assert not fi.invader_shots

    def test_dies_on_shield(self):
        fleets = Fleets()
        fi = FI(fleets)
        shield = RoadFurniture.shield(Vector2(100, 100))
        shot = InvaderShot(Vector2(100, 100), Sprite.rollers())
        assert shot.colliding(shield)
        fleets.append(shot)
        assert fi.invader_shots
        shot.interact_with_roadfurniture(shield, fleets)
        fleets.end_interactions()
        assert not fi.invader_shots

    def test_dies_on_player(self):
        fleets = Fleets()
        fi = FI(fleets)
        player = InvaderPlayer()
        player.position = Vector2(100, 100)
        shot = InvaderShot(Vector2(100, 100), Sprite.rollers())
        assert shot.colliding(player)
        fleets.append(shot)
        assert fi.invader_shots
        shot.interact_with_invaderplayer(player, fleets)
        fleets.end_interactions()
        assert not fi.invader_shots

    def test_playershot_dies_on_shield(self):
        fleets = Fleets()
        fi = FI(fleets)
        pos = Vector2(100, 100)
        shield = RoadFurniture.shield(pos)
        shot = PlayerShot(pos)
        assert shot.colliding(shield)
        fleets.append(shot)
        assert fi.player_shots
        shot.interact_with_roadfurniture(shield, fleets)
        fleets.end_interactions()
        assert not fi.player_shots
