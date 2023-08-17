import pytest
from pygame import Vector2

import u
from bitmap_maker import BitmapMaker
from fleets import Fleets
from invader_shot import InvaderShot
from tests.tools import FI


class TestInvaderShot:
    @pytest.fixture
    def shot(self):
        maker = BitmapMaker.instance()
        return InvaderShot(u.CENTER, maker.squiggles)

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
        assert shot.position == u.CENTER + Vector2(0, 4)

    def test_dies_past_edge(self, shot):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(shot)
        current_pos = u.CENTER
        while current_pos.y < u.SCREEN_SIZE:
            assert shot.position == current_pos
            current_pos = current_pos + Vector2(0, 4)
            shot.update(1/60, fleets)
            shot.update(1/60, fleets)
            shot.update(1/60, fleets)
        assert shot.position.y >= u.SCREEN_SIZE
        assert not fi.invader_shots

    def test_map_changes_on_movement(self, shot):
        fleets = Fleets()
        maps = shot.maps
        assert shot.map == maps[0]
        shot.move(fleets)
        assert shot.map == maps[1]
        shot.move(fleets)
        assert shot.map == maps[2]
        shot.move(fleets)
        assert shot.map == maps[3]
        shot.move(fleets)
        assert shot.map == maps[0]

