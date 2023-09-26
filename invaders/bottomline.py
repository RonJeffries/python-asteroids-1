import pygame.draw_py
from pygame import Rect

import u
from flyer import InvadersFlyer


class BottomLine(InvadersFlyer):

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        y = u.SCREEN_SIZE - 56
        return Rect(64, y, 960-64, 4)

    def draw(self, screen):
        pygame.draw.rect(screen, "green", self.rect)

    def interact_with(self, other, fleets):
        other.interact_with_bottomline(self, fleets)

