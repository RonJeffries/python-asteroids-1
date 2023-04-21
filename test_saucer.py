# test_saucer
from math import sin, pi

import u
from saucer import Saucer


class TestSaucer:
    def test_ready(self):
        saucer = Saucer()
        saucer.ready()
        assert saucer.position.x == 0
        assert saucer.velocity == u.SAUCER_VELOCITY
        saucer.ready()
        assert saucer.position.x == u.SCREEN_SIZE
        assert saucer.velocity == -u.SAUCER_VELOCITY

    def test_move(self):
        saucer = Saucer()
        saucer.ready()
        starting = saucer.position
        saucer.move(0.1, [])
        assert saucer.position.x == u.SAUCER_VELOCITY.x*0.1
        saucer.move(0.1, [])
        assert saucer.position.x == 2*u.SAUCER_VELOCITY.x*0.1

    def test_vanish_at_edge(self):
        saucer = Saucer()
        saucers = [saucer]
        saucer.ready()
        saucer.move(1, saucers)
        assert saucers
        while saucer.position.x < u.SCREEN_SIZE:
            assert saucers
            saucer.move(0.1, saucers)
        assert not saucers

    def test_right_to_left(self):
        saucer = Saucer()
        saucers = [saucer]
        saucer.ready()
        saucer.ready()
        assert saucer.position.x == u.SCREEN_SIZE

