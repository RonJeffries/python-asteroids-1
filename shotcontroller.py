import random

from pygame import Vector2

import u
from bitmap_maker import BitmapMaker
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
            [0x01, 0x07, 0x01, 0x01, 0x01, 0x04, 0x0B, 0x01, 0x06, 0x03, 0x01, 0x01, 0x0B, 0x09, 0x02, 0x08],
            [0x0B, 0x01, 0x06, 0x03, 0x01, 0x01, 0x0B, 0x09, 0x02, 0x08, 0x02, 0x0B, 0x04, 0x07, 0x0A, 0x01]]
        self.current_columns = [0, 0]
        self.shot_index = 0


    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def begin_interactions(self, fleets):
        self.time_since_firing += 1

    def end_interactions(self, fleets):
        if self.time_since_firing >= self.max_firing_time:
            self.fire_next_shot(fleets)

    def fire_next_shot(self, fleets):
        self.time_since_firing = 0
        shot_index = self.shot_index
        self.fire_specific_shot(shot_index, fleets)
        self.shot_index = (self.shot_index + 1) % 3

    def fire_specific_shot(self, shot_index, fleets):
        shot = self.shots[shot_index]
        if shot.position == self.available:
            shot.position = Vector2(random.randint(50, u.SCREEN_SIZE - 50), u.SCREEN_SIZE / 2)
            fleets.append(shot)

    def next_column_for(self, shot_index):
        column_number = self.current_columns[shot_index]
        self.current_columns[shot_index] = (self.current_columns[shot_index] + 1) % 16
        return self.columns[shot_index][column_number]

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderfleet(self, fleet, fleets):
        pass

    def interact_with_invaderplayer(self, player, fleets):
        pass

    def interact_with_invadershot(self, shot, fleets):
        pass

    def interact_with_playerexplosion(self, explosion, fleets):
        pass

    def interact_with_playershot(self, shot, fleets):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_shotcontroller(self, fleets)

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleets):
        pass