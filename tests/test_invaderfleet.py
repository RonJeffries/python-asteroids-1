from pygame import Vector2, Rect

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
        assert fleet.direction == +1
        assert new_pos - pos == fleet.step
        fleet.at_edge(+1)
        assert fleet.reverse
        fleet.next_invader = len(fleet.invaders)
        fleet.update(1.0, None)
        assert fleet.direction == -1

    def test_direction_reverses_at_edge(self):
        fleet = InvaderFleet()
        assert fleet.direction == +1
        fleet.at_edge(+1)
        fleet.reverse_or_continue(1.0)
        assert fleet.direction == -1

    def test_direction_unchanged_when_not_at_edge(self):
        fleet = InvaderFleet()
        assert fleet.direction == +1
        fleet.reverse_or_continue(1.0)
        assert fleet.direction == +1

    def test_step_down_at_edge(self):
        fleet = InvaderFleet()
        origin = fleet.origin
        fleet.at_edge(+1)
        fleet.reverse_or_continue(1.0)
        assert fleet.origin == origin - fleet.step + fleet.down_step, \
            "if this fails someone may have modified a vector in place"

    def test_no_step_down_when_not_at_edge(self):
        fleet = InvaderFleet()
        origin = fleet.origin
        fleet.reverse_or_continue(1.0)
        assert fleet.origin == origin + fleet.step, \
            "if this fails someone may have modified a vector in place"

    def test_bumper_intersecting_left(self):
        bumper = Bumper(64, -1)
        rect = Rect(64, 512, 64, 32)
        assert bumper.intersecting(rect)
        rect = Rect(65, 512, 64, 32)
        assert not bumper.intersecting(rect)

    def test_bumper_intersecting_right(self):
        bumper = Bumper(960, +1)
        rect = Rect(960-64, 512, 64, 32)
        assert bumper.intersecting(rect)
        rect = Rect(959-64, 512, 64, 32)
        assert not bumper.intersecting(rect)

    def test_rectangle_right(self):
        rect = Rect(100, 200, 64, 32)
        assert rect.bottomright == (164, 232)



