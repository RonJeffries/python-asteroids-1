from pygame import Vector2

import u
from core.fleets import Fleets
from invaders.invaderfleet import InvaderFleet
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
        fleets = Fleets()
        fleets.append(InvaderFleet())
        saucer.update(1.0/60.0, fleets)
        assert saucer.position.x != start.x

    def test_does_not_run_with_7_invaders(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(invader_fleet := InvaderFleet())
        invader_group = invader_fleet.invader_group
        assert invader_group.invader_count() == 55
        while invader_group.invader_count() > 7:
            invader_group.kill(invader_group.invaders[0])
        assert invader_group.invader_count() == 7
        fleets.append(saucer := InvadersSaucer())
        assert fi.invader_saucers
        saucer.interact_with_invaderfleet(invader_fleet, fleets)
        saucer.update(1.0/60.0, fleets)
        assert not fi.invader_saucers

    def test_does_run_with_8_invaders(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(invader_fleet := InvaderFleet())
        invader_group = invader_fleet.invader_group
        assert invader_group.invader_count() == 55
        while invader_group.invader_count() > 8:
            invader_group.kill(invader_group.invaders[0])
        assert invader_group.invader_count() == 8
        fleets.append(saucer := InvadersSaucer())
        assert fi.invader_saucers
        saucer.interact_with_invaderfleet(invader_fleet, fleets)
        saucer.update(1.0/60.0, fleets)
        assert fi.invader_saucers
