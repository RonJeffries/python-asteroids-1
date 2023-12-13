import pytest
from pygame import Vector2, Rect

import u
from invaders.bitmap_maker import BitmapMaker
from invaders.bumper import Bumper
from core.fleets import Fleets
from invaders.invader import Invader
from invaders.invaderfleet import InvaderFleet
from invaders.invader_group import InvaderGroup, CycleStatus
from invaders.player_shot import PlayerShot
from invaders.sprite import Sprite
from invaders.timecapsule import TimeCapsule
from tests.tools import FI, FakeFleets
from invaders.top_bumper import TopBumper


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
                assert invader.relative_position.x == x * u.INVADER_SPACING
                assert invader.relative_position.y == -y * u.INVADER_SPACING
                count += 1

    def test_fleet_origin_is_centered(self):
        fleet = InvaderFleet()
        invader = fleet.testing_only_invaders[5]  # bottom row middle column
        assert invader.position.x == 512

    def test_ok_leaves_step_alone(self):
        fleet = InvaderFleet()
        origin = fleet.origin
        fleet.process_result(CycleStatus.CONTINUE, None)
        assert fleet.origin == origin

    def test_end_increments_step(self):
        fleet = InvaderFleet()
        origin = fleet.origin
        fleet.process_result(CycleStatus.NEW_CYCLE, None)
        assert fleet.origin == origin + fleet.step

    def test_end_empty(self):
        fleets = FakeFleets()
        invader_fleet = InvaderFleet()
        invader_fleet.process_result(CycleStatus.EMPTY, fleets)
        assert invader_fleet in fleets.removes
        added = fleets.appends[0]
        assert added.time == 2
        assert isinstance(added, TimeCapsule)
        fleet = added.to_add
        assert isinstance(fleet, InvaderFleet)
        assert fleet.origin.y == 1024 - 4*u.INVADER_STARTS[0]

    def test_end_at_edge_steps_down_and_left(self):
        fleet = InvaderFleet()
        origin = fleet.origin
        direction = fleet.direction
        fleet.process_result(CycleStatus.REVERSE, None)
        assert fleet.direction == -direction
        assert fleet.origin == origin - fleet.step + fleet.down_step

    def test_rectangle_bottom_right_is_inclusive(self):
        left = 100
        top = 200
        width = 64
        height = 32
        rect = Rect(left, top, width, height)
        assert rect.bottomright == (left + width, top + height)

    def test_top_bumper(self):
        fleets = Fleets()
        fi = FI(fleets)
        bumper = TopBumper()
        shot = PlayerShot(u.CENTER)
        fleets.append(bumper)
        fleets.append(shot)
        shot.interact_with_topbumper(bumper, fleets)
        assert fi.player_shots
        # position is virtual, can't just set its y
        pos = shot.position
        pos.y = bumper.y
        shot.position = pos
        shot.interact_with_topbumper(bumper, fleets)
        fleets.end_interactions()
        assert not fi.player_shots

    def test_shot_invader_mask_collision(self):
        maker = BitmapMaker.instance()
        maps = Sprite(maker.invaders)
        invader = Invader(0, 0, maps)
        invader.position = u.CENTER
        shot = PlayerShot(Vector2(0, 0))
        offset = Vector2(shot._sprite.topleft) - Vector2(invader._sprite.topleft)
        assert not invader.mask.overlap(shot.mask, offset)
        shot.position = u.CENTER
        offset = Vector2(shot._sprite.topleft) - Vector2(invader._sprite.topleft)
        assert invader.mask.overlap(shot.mask, offset)

    def test_shot_invader_collision(self):
        maker = BitmapMaker.instance()
        maps = Sprite(maker.invaders)
        invader = Invader(0, 0, maps)
        invader_width = invader._sprite.width
        invader.position = u.CENTER
        shot = PlayerShot(Vector2(0, 0))
        shot.position = u.CENTER - Vector2(invader_width/2, 0)
        assert not invader.colliding(shot)
        shot.position = shot.position + Vector2(4, 0)
        assert not invader.colliding(shot)
        shot.position = shot.position + Vector2(4, 0)
        assert invader.colliding(shot)

    def test_shot_removes_itself(self):
        fleets = Fleets()
        fi = FI(fleets)
        shot = PlayerShot()
        fleets.append(shot)
        assert fi.player_shots
        fleets.begin_interactions()
        shot.hit_invader(self, fleets)
        fleets.end_interactions()
        assert not fi.player_shots

    def test_start_conversion(self):
        fleet = InvaderFleet()
        start = fleet.convert_y_coordinate(u.INVADER_FIRST_START)
        should = 1024 - 4*u.INVADER_FIRST_START
        assert start == should

    def test_initial_fleet_y(self):
        fleet = InvaderFleet()
        starting_y = fleet.origin.y
        assert starting_y == 1024 - 4*u.INVADER_FIRST_START

    def test_initial_fleet_y_with_parameter(self):
        fleet = InvaderFleet(-1)
        starting_y = fleet.origin.y
        assert starting_y == 1024 - 4*u.INVADER_FIRST_START

    def test_initial_fleet_y_given_0_parameter(self):
        fleet = InvaderFleet(0)
        starting_y = fleet.origin.y
        assert starting_y == 1024 - 4*u.INVADER_STARTS[0]

    def test_initial_fleet_y_given_8_parameter(self):
        fleet = InvaderFleet(8)
        starting_y = fleet.origin.y
        assert starting_y == 1024 - 4*u.INVADER_STARTS[0]

    def test_fleet_after_initial_is_0_fleet(self):
        fleet = InvaderFleet(-1)
        assert fleet.origin.y == 1024 - 4*u.INVADER_FIRST_START
        fleet = fleet.next_fleet()
        assert fleet.origin.y == 1024 - 4*u.INVADER_STARTS[0]
        fleet = fleet.next_fleet()
        assert fleet.origin.y == 1024 - 4*u.INVADER_STARTS[1]

    def test_fleet_starting_values_including_wrap(self):
        fleet = InvaderFleet(-1)
        assert fleet.origin.y == 1024 - 4*u.INVADER_FIRST_START
        for i in range(len(u.INVADER_STARTS)):
            fleet = fleet.next_fleet()
            assert fleet.origin.y == 1024 - 4*u.INVADER_STARTS[i]
        fleet = fleet.next_fleet()
        assert fleet.origin.y == 1024 - 4*u.INVADER_STARTS[0]

    def test_loop_indexing(self):
        init = -1
        for i in range(9):
            init = (init + 1) % 8
        assert init == 0








