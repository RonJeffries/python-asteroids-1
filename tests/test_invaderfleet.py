from pygame import Vector2, Rect

import u
from bumper import Bumper
from invader import INVADER_SPACING, Invader
from invaderfleet import InvaderFleet, InvaderGroup


class TestInvaderFleet:
    def test_exists(self):
        fleet = InvaderFleet()

    def test_makes_invaders(self):
        fleet = InvaderFleet()
        invaders = fleet.testing_only_invaders
        assert len(invaders) == 55

    def test_invaders_order(self):
        fleet = InvaderFleet()
        count = 0
        for y in range(5):
            for x in range(11):
                invader = fleet.testing_only_invaders[count]
                assert invader.relative_position.x == x * INVADER_SPACING
                assert invader.relative_position.y == -y * INVADER_SPACING
                count += 1

    def test_fleet_origin_is_centered(self):
        fleet = InvaderFleet()
        assert fleet.origin == Vector2(u.SCREEN_SIZE / 2 - 5*64, 512)
        invader = fleet.testing_only_invaders[5]  # bottom row middle column
        assert invader.position.x == 512

    def test_fleet_y_decreases_with_n(self):
        group = InvaderGroup()
        group.position_all_invaders(Vector2(0, 0))
        first: Invader = group.invaders[0]
        last: Invader = group.invaders[-1]
        assert first.position.y > last.position.y

    def test_fleet_motion(self):
        fleet = InvaderFleet()
        fleet.step = Vector2(30, 0)
        pos = fleet.testing_only_invaders[0].position
        fleet.update(1.0, None)
        new_pos = fleet.testing_only_invaders[0].position
        assert fleet.direction == +1
        assert new_pos - pos == fleet.step
        fleet.at_edge(+1)
        assert fleet.reverse
        fleet.next_invader = len(fleet.testing_only_invaders)
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

    def test_rectangle_bottom_right_is_inclusive(self):
        left = 100
        top = 200
        width = 64
        height = 32
        rect = Rect(left, top, width, height)
        assert rect.bottomright == (left + width, top + height)



