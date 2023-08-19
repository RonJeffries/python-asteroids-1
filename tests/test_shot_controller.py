import u
from bitmap_maker import BitmapMaker
from fleets import Fleets
from invader_shot import InvaderShot
from shotcontroller import ShotController
from tests.tools import FI


class TestShotController:
    def test_exists(self):
        ShotController()

    def test_tracks_cycles(self):
        fleets = Fleets()
        maker = BitmapMaker.instance()
        shot = InvaderShot(u.CENTER, maker.squiggles)
        controller = ShotController()
        assert controller.time_since_firing == 0
        controller.begin_interactions(fleets)
        assert controller.time_since_firing == 1

    def test_fires_shot(self):
        fleets = Fleets()
        fi = FI(fleets)
        controller = ShotController()
        assert not fi.invader_shots
        controller.begin_interactions(fleets)
        controller.time_since_firing = controller.max_firing_time
        controller.end_interactions(fleets)
        assert fi.invader_shots

    def test_fires_three_different_shots(self):
        fleets = Fleets()
        fi = FI(fleets)
        controller = ShotController()
        for _ in range(3):
            controller.fire_next_shot(fleets)
        shots = fi.invader_shots
        assert len(shots) == 3
        s1, s2, s3 = shots
        assert s1.map != s2.map and s2.map != s3.map and s3.map != s1.map
        assert s1.position != ShotController.available
        assert s2.position != ShotController.available
        assert s2.position != ShotController.available
        controller.fire_next_shot(fleets)
        assert len(fi.invader_shots) == 3
        s1.die(fleets)
        s2.die(fleets)
        s3.die(fleets)
        assert len(fi.invader_shots) == 0
        for _ in range(3):
            controller.fire_next_shot(fleets)
        assert len(fi.invader_shots) == 3

    def test_plunger_columns(self):
        controller = ShotController()
        assert controller.next_column_for(0) == 0x01
        assert controller.next_column_for(0) == 0x07
        assert controller.next_column_for(1) == 0x0B
        assert controller.next_column_for(1) == 0x01
        for _ in range(14):
            controller.next_column_for(1)
        assert controller.next_column_for(1) == 0x0B


