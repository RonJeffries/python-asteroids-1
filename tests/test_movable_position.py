from pygame import Vector2

import u
from asteroids.movable_location import MovableLocation


class TestMovablePosition:
    def test_creation(self):
        position = Vector2(0, 0)
        velocity = Vector2(100, 200)
        MovableLocation(position, velocity)

    def test_motion(self):
        position = Vector2(0, 0)
        velocity = Vector2(100, 200)
        mp = MovableLocation(position, velocity)
        mp.move(0.25)
        assert mp.position == Vector2(25, 50)

    def test_motion_wraps(self):
        position = Vector2(990, 990)
        velocity = Vector2(100, 200)
        mp = MovableLocation(position, velocity, 1000)
        mp.move(0.25)
        assert mp.position == Vector2(15, 40)

    def test_acceleration(self):
        position = Vector2(990, 990)
        velocity = Vector2(100, 200)
        mp = MovableLocation(position, velocity, 1000)
        mp.accelerate_by(Vector2(15, 37))
        assert mp.velocity == Vector2(115, 237)

    def test_wrap_booleans(self):
        position = Vector2(990, 990)
        velocity = Vector2(100, 50)
        mp = MovableLocation(position, velocity, 1000)
        off_x, off_y = mp.move(0.05)
        assert not off_x
        assert not off_y
        off_x, off_y = mp.move(0.05)
        assert off_x
        assert not off_y
        off_x, off_y = mp.move(0.1)
        assert not off_x
        assert off_y

    def test_moving_away_from_point(self):
        center = u.CENTER
        position = center + Vector2(10, 10)
        velocity = Vector2(1, 1)
        ml = MovableLocation(position, velocity)
        assert ml.moving_away_from(u.CENTER)
        m2 = MovableLocation(center + Vector2(10, -10), Vector2(-1, 1))
        assert not m2.moving_away_from(u.CENTER)

