from pygame import Vector2

import u
from invaders.bitmap_maker import BitmapMaker
from invaders.bumper import Bumper
from invaders.invader import Invader
from invaders.invader_group import InvaderGroup, CycleStatus
from invaders.invader_player import InvaderPlayer
from invaders.roadfurniture import RoadFurniture
from invaders.sprite import Sprite
from tests.tools import FakeFleets


class TestInvaderGroup:
    def test_exists(self):
        InvaderGroup()

    def test_invader_position(self):
        maker = BitmapMaker.instance()
        maps = Sprite(maker.invaders)
        invader = Invader(1, 1, maps)
        assert invader.position == Vector2(32, 16)
        invader.move_relative_to(Vector2(111, 222))
        assert invader.position == Vector2(111, 222) + Vector2(64, -64)

    def test_fleet_y_decreases_with_n(self):
        group = InvaderGroup()
        group.position_all_invaders(Vector2(0, 0))
        first: Invader = group.invaders[0]
        last: Invader = group.invaders[-1]
        assert first.position is not last.position
        assert first.position.y > last.position.y

    def test_update_next(self):
        group = InvaderGroup()
        origin = Vector2(100, 100)
        for i in range(55):
            result = group.update_next(origin)
            assert result == CycleStatus.CONTINUE
        result = group.update_next(origin)
        assert result == CycleStatus.NEW_CYCLE

    def test_no_reversal(self):
        group = InvaderGroup()
        group.position_all_invaders(Vector2(u.BUMPER_LEFT + 100, 512))
        result = group.end_cycle()
        assert result == CycleStatus.NEW_CYCLE

    def test_reversal(self):
        group = InvaderGroup()
        bumper = Bumper(u.BUMPER_RIGHT, +1)
        invader = group.invaders[0]
        _pos_x, pos_y = invader.position
        invader.position = (u.BUMPER_RIGHT, pos_y)
        result = group.end_cycle()
        assert result == CycleStatus.REVERSE
        invader.position = (u.BUMPER_LEFT, pos_y)
        assert result == CycleStatus.REVERSE

    def test_too_low(self):
        group = InvaderGroup()
        group.position_all_invaders(Vector2(u.SCREEN_SIZE / 2 - 5 * 64, 0x78))
        invader = group.invaders[0]
        _pos_x, pos_y = invader.position
        invader.position = (_pos_x, u.INVADER_TOO_FAR_DOWN_Y + 1)
        result = group.end_cycle()
        assert result == CycleStatus.TOO_LOW

    def test_remove_penultimate_invader(self):
        group = InvaderGroup()
        for count in range(54):
            group.kill(group.invaders[0])
        result = group.update_next(Vector2(0, 0))
        result = group.update_next(Vector2(0, 0))
        assert result == CycleStatus.NEW_CYCLE

    def test_remove_last_invader(self):
        group = InvaderGroup()
        for count in range(55):
            group.kill(group.invaders[0])
        result = group.update_next(Vector2(0, 0))
        assert result == CycleStatus.EMPTY

    def test_bottom_of_column(self):
        group = InvaderGroup()
        invader = group.bottom_of_column(5)
        assert invader.column == 5
        for i in range(5):
            invader = group.bottom_of_column(5)
            group.kill(invader)
        invader = group.bottom_of_column(5)
        assert not invader

    def test_remove_ahead_of_cursor(self):
        group = InvaderGroup()
        to_remove = group.invaders[23]
        next = group.next_invader()
        group.kill(to_remove)
        assert group.next_invader() == next

    def test_remove_at_cursor(self):
        group = InvaderGroup()
        to_remove = group.invaders[23]
        group._next_invader = 23
        should_update = group.invaders[24]
        next_up = group.next_invader()
        assert next_up == to_remove
        group.kill(to_remove)
        assert group.next_invader() == should_update

    def test_remove_after_cursor(self):
        group = InvaderGroup()
        to_remove = group.invaders[23]
        group._next_invader = 30
        should_update = group.invaders[30]
        group.kill(to_remove)
        assert group.next_invader() == should_update

    def test_invader_bounds(self):
        maker = BitmapMaker.instance()
        sprite = Sprite(maker.invaders)
        invader = Invader(1, 1, sprite)
        invader.position = Vector2(100, 500)
        assert not invader.is_out_of_bounds(90, 1000)
        assert invader.is_out_of_bounds(110, 1000)
        assert invader.is_out_of_bounds(80, 90)

    def test_invader_damages_shield(self):
        maker = BitmapMaker.instance()
        sprite = Sprite(maker.invaders)
        invader = Invader(1, 1, sprite)
        shield = RoadFurniture.shield(Vector2(242, 816))
        assert not invader.colliding(shield)
        invader.position = shield.position
        assert invader.colliding(shield)
        old_mask = shield.sprite.mask
        invader.interact_with_roadfurniture(shield, None)
        assert shield.sprite.mask is not old_mask

    def test_invader_kills_player(self):
        maker = BitmapMaker.instance()
        sprite = Sprite(maker.invaders)
        invader = Invader(1, 1, sprite)
        player = InvaderPlayer()
        fleets = FakeFleets()
        invader.interact_with_invaderplayer(player, fleets)
        assert not fleets.removes
        invader.position = player.position
        invader.interact_with_invaderplayer(player, fleets)
        assert fleets.removes
        assert player in fleets.removes
