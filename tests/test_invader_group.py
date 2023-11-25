from pygame import Vector2

import u
from invaders.bitmap_maker import BitmapMaker
from invaders.bumper import Bumper
from invaders.invader import Invader
from invaders.invader_group import InvaderGroup, CycleStatus


class TestInvaderGroup:
    def test_exists(self):
        InvaderGroup()

    def test_invader_position(self):
        maker = BitmapMaker.instance()
        maps = maker.invaders
        invader = Invader(1, 1, maps)
        assert invader.position == Vector2(32, 16)
        invader.position = Vector2(111, 222)
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
            result = group.update_next(origin, 1)
            assert result == CycleStatus.CONTINUE
        result = group.update_next(origin, 1)
        assert result == CycleStatus.NEW_CYCLE

    def test_no_reversal(self):
        group = InvaderGroup()
        bumper = Bumper(u.BUMPER_RIGHT, +1)
        group.interact_with_bumper(bumper, None)
        result = group.end_cycle()
        assert result == CycleStatus.NEW_CYCLE

    def test_reversal_on_entry(self):
        group = InvaderGroup()
        bumper = Bumper(u.BUMPER_RIGHT, +1)
        invader = group.invaders[0]
        _pos_x, pos_y = invader.position
        invader.position = (u.BUMPER_RIGHT, pos_y)
        group.testing_set_to_end()
        group.interact_with_bumper(bumper, None)
        result = group.end_cycle()
        assert result == CycleStatus.REVERSE

        origin = (0, 0)
        result = CycleStatus.CONTINUE
        while result == CycleStatus.CONTINUE:
            invader.position = (u.BUMPER_RIGHT, pos_y)
            result = group.update_next(origin, -1)
        assert result == CycleStatus.NEW_CYCLE

    def test_no_reversal_on_exit(self):
        group = InvaderGroup()
        group.current_direction = -1
        bumper = Bumper(u.BUMPER_RIGHT, +1)
        invader = group.invaders[0]
        _pos_x, pos_y = invader.position
        invader.position = (u.BUMPER_RIGHT, pos_y)
        group.interact_with_bumper(bumper, None)
        result = group.end_cycle()
        assert result == CycleStatus.NEW_CYCLE

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

    def test_remove_last_invader(self):
        group = InvaderGroup()
        for count in range(55):
            group.kill(group.invaders[0])
        result = group.update_next(Vector2(0, 0), 1)
        assert result == CycleStatus.NEW_CYCLE


