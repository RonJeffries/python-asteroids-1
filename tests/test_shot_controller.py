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
