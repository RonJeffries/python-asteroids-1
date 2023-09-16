import pygame
from pygame import Rect

import u
from flyer import InvadersFlyer
from ignorethese import IgnoreThese


class Bumper(InvadersFlyer,
             metaclass=IgnoreThese,
             ignore=["interact_with_bumper",
                     "interact_with_invaderexplosion",
                     "interact_with_invaderfleet",
                     "interact_with_invaderplayer",
                     "interact_with_invadershot",
                     "interact_with_playerexplosion",
                     "interact_with_shield",
                     "interact_with_playershot",
                     "interact_with_shotcontroller",
                     "interact_with_shotexplosion",
                     "interact_with_topbumper"]):
    def __init__(self, x, incoming_direction):
        self.x = x
        self.check = self.beyond_on_right if incoming_direction > 0 else self.beyond_on_left
        self.incoming_direction = incoming_direction

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def intersecting(self, rect: Rect):
        return self.check(rect)

    def beyond_on_left(self, rect):
        return rect.bottomleft[0] <= self.x

    def beyond_on_right(self, rect):
        return rect.bottomright[0] >= self.x

    def interact_with(self, other, fleets):
        other.interact_with_bumper(self, fleets)

    def draw(self, screen):
        pygame.draw.line(screen, "green", (self.x, 0), (self.x, u.SCREEN_SIZE))

    def tick(self, delta_time, fleets):
        pass
