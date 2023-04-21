# test_saucer
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
        saucer.move(u.SCREEN_SIZE/u.SAUCER_VELOCITY.x, saucers)
        assert saucer.position.x > u.SCREEN_SIZE
        assert not saucers

    def test_right_to_left(self):
        saucer = Saucer()
        saucers = [saucer]
        saucer.ready()
        saucer.ready()
        assert saucer.position.x == u.SCREEN_SIZE

    def test_zig_zag_directions(self):
        saucer = Saucer()
        straight = u.SAUCER_VELOCITY
        up = straight.rotate(45)
        down = straight.rotate(-45)
        assert saucer.new_direction(0) == up
        assert saucer.new_direction(1) == straight
        assert saucer.new_direction(2) == straight
        assert saucer.new_direction(3) == down
        assert saucer.new_direction(4) == up
        assert saucer.new_direction(5) == straight
        assert saucer.new_direction(-1) == down
