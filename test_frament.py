from pygame import Vector2

import u
from fleet import ExplosionFleet
from fleets import Fleets
from fragment import Fragment


class TestFragments():
    def test_frag(self):
        frag = Fragment(position = u.CENTER)
        assert frag

    def test_frag_random_angle(self):
        angle = 180
        frag = Fragment(position = u.CENTER, angle=angle)
        assert frag.velocity == Vector2(u.FRAGMENT_SPEED, 0).rotate(angle)
        assert frag.velocity.x == -u.FRAGMENT_SPEED

    def test_frag_timeout(self):
        frag = Fragment(position = u.CENTER)
        fleets = Fleets()
        frags = fleets.explosions
        frags.append(frag)
        frags.tick(0.1, fleets)
        assert frags
        frags.tick(u.FRAGMENT_LIFETIME, fleets)
        assert not frags

    def test_fragment_move(self):
        frag = Fragment(position=u.CENTER, angle=0)
        assert frag.velocity == Vector2(u.FRAGMENT_SPEED, 0)
        frag.move(0.1)
        assert frag.position == u.CENTER + Vector2(u.FRAGMENT_SPEED*0.1, 0)

