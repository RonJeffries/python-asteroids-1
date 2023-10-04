from pygame import Vector2

from invaders.invaders_saucer import InvadersSaucer, InvadersSaucerMaker


class TestInvadersSaucer:
    def test_exists(self):
        InvadersSaucer()

    def test_maker_exists(self):
        InvadersSaucerMaker()

    def test_saucer_moves(self):
        saucer = InvadersSaucer(1)
        left_side_start = Vector2(64, 128)
        assert saucer.position == left_side_start
        saucer.update(1.0/60.0, [])
        assert saucer.position.x > left_side_start.x
