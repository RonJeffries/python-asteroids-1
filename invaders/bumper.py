import pygame
from pygame import Rect

import u
from flyer import InvadersFlyer


class Bumper(InvadersFlyer):
    def __init__(self, x, incoming_direction):
        self.x = x
        self.incoming_direction = incoming_direction

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def intersecting(self, rect: Rect):
        return self.beyond_on_right(rect) if self.incoming_direction > 0 else self.beyond_on_left(rect)

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
