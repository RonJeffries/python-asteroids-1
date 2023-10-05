from pygame import Vector2

import u
from core.fleets import Fleets
from invaders.invaders_saucer import InvadersSaucer, InvadersSaucerMaker
from tests.tools import FI


class TestInvadersSaucer:
    def test_exists(self):
        InvadersSaucer()

    def test_maker_exists(self):
        InvadersSaucerMaker()

    def test_saucer_moves(self):
        saucer = InvadersSaucer()
        start = saucer.position
        saucer.update(1.0/60.0, [])
        assert saucer.position.x != start.x

    def test_runs_with_8_Invaders(self):
        fleets = Fleets()
        fi = FI(Fleets)
        fleets.append(saucer := InvadersSaucer())
        start = saucer.position
        saucer.begin_interactions(fleets)
        invader = In
        for _ in range(8):
            saucer.interact_with_invader(invader, fleets)
        saucer.update(1.0/60.0, fleets)
        assert saucer.position != start
