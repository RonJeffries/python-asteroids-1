from pygame import Vector2

import u
from fleets import Fleets
from fragment import Fragment
from test_interactions import FI


class TestFragments:
    def test_frag(self):
        frag = Fragment(position=u.CENTER, fragments=["ignored"])
        assert frag

    def test_frag_random_angle(self):
        angle = 180
        frag = Fragment(position=u.CENTER, angle=angle, speed_mul=1, fragments=["ignored"])
        assert frag.velocity == Vector2(u.FRAGMENT_SPEED, 0).rotate(angle)
        assert frag.velocity.x == -u.FRAGMENT_SPEED

    def test_frag_timeout(self):
        frag = Fragment(position=u.CENTER, fragments=["ignored"])
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(frag)
        fleets.tick(0.1)
        assert fi.fragments
        fleets.tick(u.FRAGMENT_LIFETIME)
        assert not fi.fragments

    def test_fragment_move(self):
        frag = Fragment(position=u.CENTER, angle=0, speed_mul=1, fragments=["ignored"])
        assert frag.velocity == Vector2(u.FRAGMENT_SPEED, 0)
        frag.update(0.1, [])
        assert frag.position == u.CENTER + Vector2(u.FRAGMENT_SPEED * 0.1, 0)
