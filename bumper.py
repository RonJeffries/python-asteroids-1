import pygame
from pygame import Rect

import u
from flyer import Flyer


class Bumper(Flyer):
    def __init__(self, x, incoming_direction):
        self.x = x
        self.incoming_direction = incoming_direction

    def intersecting(self, rect: Rect):
        if self.incoming_direction > 0:
            return rect.bottomright[0] >= self.x
        else:
            return rect.bottomleft[0] <= self.x

    def interact_with_invaderfleet(self, invader, fleets):
        pass

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_bumper(self, fleets)

    def draw(self, screen):
        pygame.draw.line(screen, "green", (self.x, 0), (self.x, u.SCREEN_SIZE))

    def tick(self, delta_time, fleets):
        pass

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass
