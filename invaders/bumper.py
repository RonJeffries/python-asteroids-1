import pygame
from pygame import Rect

import u
from flyer import InvadersFlyer
from invaders.sprite import Sprite


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

    def am_i_entering(self, rect):
        return self.intersecting(rect)

    def intersecting(self, sprite: Sprite):
        return self.beyond_on_right(sprite) if self.incoming_direction > 0 else self.beyond_on_left(sprite)

    def beyond_on_left(self, sprite):
        return sprite.centerx <= self.x

    def beyond_on_right(self, sprite):
        return sprite.centerx >= self.x

    def interact_with(self, other, fleets):
        other.interact_with_bumper(self, fleets)

    def draw(self, screen):
        pygame.draw.line(screen, "green", (self.x, 0), (self.x, u.SCREEN_SIZE))

    def tick(self, delta_time, fleets):
        pass
