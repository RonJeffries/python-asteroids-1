from pygame import Vector2

from invader import Invader
from invaderfleet import InvaderGroup


class TestInvaderGroup:
    def test_exists(self):
        InvaderGroup()

    def test_fleet_y_decreases_with_n(self):
        group = InvaderGroup()
        group.position_all_invaders(Vector2(0, 0))
        first: Invader = group.invaders[0]
        last: Invader = group.invaders[-1]
        assert first.position.y > last.position.y

    def test_update_next(self):
        group = InvaderGroup()
        origin = Vector2(100, 100)
        for i in range(54):
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

