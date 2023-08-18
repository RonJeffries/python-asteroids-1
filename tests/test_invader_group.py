from pygame import Vector2

from bitmap_maker import BitmapMaker
from invader import Invader
from invader_group import InvaderGroup


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
            result = group.update_next(origin)
            assert result == "ok"
        result = group.update_next(origin)
        assert result == "end"

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
        result = group.update_next(Vector2(0, 0))
        assert result == "end"


