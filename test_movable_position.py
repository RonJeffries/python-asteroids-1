from pygame import Vector2

from movable_position import MovablePosition


class TestMovablePosition:
    def test_creation(self):
        position = Vector2(0, 0)
        velocity = Vector2(100, 200)
        mp = MovablePosition(position, velocity)