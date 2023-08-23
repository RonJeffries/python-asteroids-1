import random

from pygame import Vector2

import u
from bitmap_maker import BitmapMaker
from cycler import Cycler
from flyer import InvadersFlyer
from invader_shot import InvaderShot


class ShotController(InvadersFlyer):
    max_firing_time = 0x30
    available = Vector2(-1, -1)

    def __init__(self):
        self.time_since_firing = 0
        self.shots = [
            InvaderShot(self.available, BitmapMaker.instance().squiggles),
            InvaderShot(self.available, BitmapMaker.instance().rollers),
            InvaderShot(self.available, BitmapMaker.instance().plungers)]
        self.columns = [
            Cycler([0x00, 0x06, 0x00, 0x00, 0x00, 0x03, 0x0A, 0x00, 0x05, 0x02, 0x00, 0x00, 0x0A, 0x08, 0x01, 0x07]),
            Cycler([0x0A, 0x00, 0x05, 0x02, 0x00, 0x00, 0x0A, 0x08, 0x01, 0x07, 0x01, 0x0A, 0x03, 0x06, 0x09])]
        self.shot_index = 0
        self.invader_fleet = None
        self.player_x = 0

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    @property
    def fleet_x(self):
        return self.invader_fleet.origin.x

    def begin_interactions(self, fleets):
        self.time_since_firing += 1

    def end_interactions(self, fleets):
        if self.time_since_firing >= self.max_firing_time:
            self.fire_next_shot(fleets)

    def fire_next_shot(self, fleets):
        self.time_since_firing = 0
        shot_index = self.shot_index
        self.fire_specific_shot(shot_index, fleets)

    def fire_specific_shot(self, shot_index, fleets):
        shot = self.shots[shot_index]
        if shot.position == self.available:
            pos = self.select_shot_position(shot, shot_index)
            if pos:
                shot.position = pos
                fleets.append(shot)
            self.shot_index = (self.shot_index + 1) % 3

    def select_shot_position(self, shot, shot_index):
        if shot_index == 2:
            col = self.target_column(self.player_x, self.fleet_x)
        else:
            col = self.next_column_for(shot_index)
        invader = self.invader_fleet.invader_group.bottom_of_column(col)
        if invader:
            return invader.position
        else:
            return None

    def next_column_for(self, shot_index):
        return self.columns[shot_index].next()

    def target_column(self, player_x, fleet_x):
        steps = round((player_x - fleet_x) / 64)
        return max(0, min(steps, 10))

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderexplosion(self, explosion, fleets):
        pass

    def interact_with_invaderfleet(self, fleet, fleets):
        self.invader_fleet = fleet

    def interact_with_invaderplayer(self, player, fleets):
        self.player_x = player.position.x

    def interact_with_invadershot(self, shot, fleets):
        pass

    def interact_with_playerexplosion(self, explosion, fleets):
        pass

    def interact_with_playershot(self, shot, fleets):
        pass

    def interact_with_shotcontroller(self, controller, fleets):
        pass

    def interact_with_shotexplosion(self, bumper, fleets):
        pass

    def interact_with_topbumper(self, top_bumper, fleets):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_shotcontroller(self, fleets)

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleets):
        pass