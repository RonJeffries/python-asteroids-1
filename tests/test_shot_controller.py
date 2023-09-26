from pygame import Vector2

import u
from invaders.bitmap_maker import BitmapMaker
from core.fleets import Fleets
from flyer import InvadersFlyer
from invaders.invader_player import InvaderPlayer
from invaders.invader_shot import InvaderShot
from invaders.invaderfleet import InvaderFleet
from invaders.shotcontroller import ShotController
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
        invader_fleet = InvaderFleet()
        fleets.append(invader_fleet)
        controller = ShotController()
        assert not fi.invader_shots
        controller.begin_interactions(fleets)
        controller.interact_with_invaderfleet(invader_fleet, fleets)
        controller.time_since_firing = controller.max_firing_time
        controller.end_interactions(fleets)
        assert fi.invader_shots

    def test_fires_three_different_shots(self):
        fleets = Fleets()
        fi = FI(fleets)
        controller = ShotController()
        invader_fleet = InvaderFleet()
        controller.invader_fleet = invader_fleet
        for _ in range(3):
            controller.fire_next_shot(fleets)
        shots = fi.invader_shots
        assert len(shots) == 3
        s1, s2, s3 = shots
        assert s1._map != s2._map and s2._map != s3._map and s3._map != s1._map
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
        desired = controller.columns[1]._values
        for i in range(22):
            col = controller.next_column_for(1)
            index = i % len(desired)
            assert col == desired[index]

    def test_targeting(self):
        controller = ShotController()
        player_x = 100
        fleet_x = 0
        # 0 64 128 192 256
        assert controller.target_column(player_x, fleet_x) == 2
        fleet_x = 192  # past him, can't hit
        assert controller.target_column(player_x, fleet_x) == 0  # -1 actually
        fleet_x = 64  # hard left
        player_x = 950  # way off to right
        assert controller.target_column(player_x, fleet_x) == 10  # 14 actually

    def test_captures_fleet_x(self):
        fleets = Fleets()
        invader_fleet = InvaderFleet()
        invader_fleet.origin = Vector2(123, 456)
        controller = ShotController()
        controller.begin_interactions(fleets)
        controller.interact_with_invaderfleet(invader_fleet, fleets)
        assert controller.fleet_x == 123

    def test_captures_player_x(self):
        fleets = Fleets()
        player = InvaderPlayer()
        position = player.position
        controller = ShotController()
        controller.begin_interactions(player)
        controller.interact_with_invaderplayer(player, fleets)
        assert controller.player_x == position.x

    def test_print_subclasses(self):
        subs = InvadersFlyer.__subclasses__()
        names = [sub.__name__ for sub in subs]
        names.sort()
        for name in names:
            print("| " + name, end="")
        print(" |",)
        # assert False

    def test_print_dictionaries(self):
        subs = InvadersFlyer.__subclasses__()
        names = [sub.__name__ for sub in subs]
        names.sort()
        for name in names:
            self.print_dict(name, names)
        # assert False

    def print_dict(self, name, names):
        print(name + ": {")
        for name in names:
            print("    " + name + ":error,")
        print("},")




