import pygame
from pygame import Rect

import u
from flyer import InvadersFlyer


class Bumper(InvadersFlyer):
    def __init__(self, x, incoming_direction):
        self.x = x
        self.check = self.beyond_on_right if incoming_direction > 0 else self.beyond_on_left
        self.incoming_direction = incoming_direction

    def intersecting(self, rect: Rect):
        return self.check(rect)

    def beyond_on_left(self, rect):
        return rect.bottomleft[0] <= self.x

    def beyond_on_right(self, rect):
        return rect.bottomright[0] >= self.x

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderfleet(self, invader, fleets):
        pass

    def interact_with_invaderplayer(self, invader, fleets):
        pass

    def interact_with_playershot(self, bumper, fleets):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_bumper(self, fleets)

    def draw(self, screen):
        pygame.draw.line(screen, "green", (self.x, 0), (self.x, u.SCREEN_SIZE))

    def tick(self, delta_time, fleets):
        pass
