import random

from pygame import Vector2

import u
from bitmap_maker import BitmapMaker
from flyer import InvadersFlyer
from invader_shot import InvaderShot


class ShotController(InvadersFlyer):
    max_firing_time = 0x30

    def __init__(self):
        self.time_since_firing = 0

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
            self.time_since_firing = 0
            pos = Vector2(random.randint(50, u.SCREEN_SIZE - 50), u.SCREEN_SIZE / 2)
            shot = InvaderShot(pos, BitmapMaker.instance().squiggles)
            fleets.append(shot)

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