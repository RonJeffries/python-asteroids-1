from pygame import Vector2

import u
from invaders.invaders_saucer import InvadersSaucer, InvadersSaucerMaker


class TestInvadersSaucer:
    def test_exists(self):
        InvadersSaucer()

    def test_maker_exists(self):
        InvadersSaucerMaker()

    def test_saucer_moves(self):
        saucer = InvadersSaucer(1)
        start = saucer.position
        saucer.update(1.0/60.0, [])
        assert saucer.position.x != start.x
