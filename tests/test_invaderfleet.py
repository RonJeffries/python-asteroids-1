from pygame import Vector2, Rect

import u
from invaders.bitmap_maker import BitmapMaker
from invaders.bumper import Bumper
from core.fleets import Fleets
from invaders.invader import INVADER_SPACING, Invader
from invaders.invaderfleet import InvaderFleet
from invaders.invader_group import InvaderGroup, CycleStatus
from invaders.player_shot import PlayerShot
from tests.tools import FI
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
                assert invader.relative_position.x == x * INVADER_SPACING
                assert invader.relative_position.y == -y * INVADER_SPACING
                count += 1

    def test_fleet_origin_is_centered(self):
        fleet = InvaderFleet()
        assert fleet.origin == Vector2(u.SCREEN_SIZE / 2 - 5*64, 512) + Vector2(8, 0)
        invader = fleet.testing_only_invaders[5]  # bottom row middle column
        assert invader.position.x == 512

    def test_ok_leaves_step_alone(self):
        fleet = InvaderFleet()
        origin = fleet.origin
        fleet.process_result(CycleStatus.CONTINUE)
        assert fleet.origin == origin

    def test_end_increments_step(self):
        fleet = InvaderFleet()
        origin = fleet.origin
        fleet.process_result(CycleStatus.NEW_CYCLE)
        assert fleet.origin == origin + fleet.step

    def test_end_at_edge_steps_down_and_left(self):
        fleet = InvaderFleet()
        origin = fleet.origin
        direction = fleet.direction
        fleet.process_result(CycleStatus.REVERSE)
        assert fleet.direction == -direction
        assert fleet.origin == origin - fleet.step + fleet.down_step

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

    def test_invader_bitmaps(self):
        maps = InvaderGroup.create_invader_bitmaps(None)
        assert len(maps) == 5
        first = maps[0]
        assert len(first) == 2
        assert first[0] != first[1]
        # assert False

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
        maps = maker.invaders
        invader = Invader(0, 0, maps)
        invader.position = u.CENTER
        shot = PlayerShot(Vector2(0, 0))
        offset = Vector2(shot.rect.topleft) - Vector2(invader.rect.topleft)
        assert not invader.mask.overlap(shot.mask, offset)
        shot.position = u.CENTER
        offset = Vector2(shot.rect.topleft) - Vector2(invader.rect.topleft)
        assert invader.mask.overlap(shot.mask, offset)

    def test_shot_invader_collision(self):
        maker = BitmapMaker.instance()
        maps = maker.invaders
        invader = Invader(0, 0, maps)
        invader_width = invader.rect.width
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
        shot.hit_invader(fleets)
        fleets.end_interactions()
        assert not fi.player_shots








