from pygame import Vector2

import u
from bumper import Bumper
from invader import Invader
from invaderfleet import InvaderFleet


class TestInvaderFleet:
    def test_exists(self):
        fleet = InvaderFleet()

    def test_makes_invaders(self):
        fleet = InvaderFleet()
        invaders = fleet.invaders
        assert len(invaders) == 55

    def test_invaders_order(self):
        fleet = InvaderFleet()
        count = 0
        for y in range(5):
            for x in range(11):
                invader = fleet.invaders[count]
                assert invader.row == x
                assert invader.column == y
                count += 1

    def test_fleet_origin(self):
        fleet = InvaderFleet()
        assert fleet.origin == Vector2(u.SCREEN_SIZE / 2 - 5*64, 512)
        invader = fleet.invaders[5]  # bottom row middle column
        assert invader.position.x == 512

    def test_fleet_motion(self):
        fleet = InvaderFleet()
        fleet.step = Vector2(30, 0)
        pos = fleet.invaders[0].position
        fleet.update(1.0, None)
        new_pos = fleet.invaders[0].position
        assert new_pos - pos == fleet.step
        fleet.at_edge()
        fleet.end_interactions(None)
        assert fleet.step == (Vector2(-30, 0))

    def test_bumper_invader_collision(self):
        fleet = InvaderFleet()
        bumper_x = 16
        bumper = Bumper(bumper_x)
        invader_column = 5
        invader = Invader(invader_column, 2)
        start = Vector2(64, 512)
        step = 64
        invader.move_relative(fleet.origin)
        invader.interact_with_bumper(bumper, fleet)
        assert not fleet.reverse
        start_x = bumper_x - invader_column*step
        start = Vector2(start_x, 512)
        invader.move_relative(start)
        invader.interact_with_bumper(bumper, fleet)
        assert fleet.reverse


