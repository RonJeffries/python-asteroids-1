import pygame
from pygame import Vector2

import u
from bitmap_maker import BitmapMaker
from flyer import InvadersFlyer
from movable_location import MovableLocation


class PlayerShot(InvadersFlyer):
    def __init__(self, position=u.CENTER):
        offset = Vector2(0, -8*4)
        self.position = position + offset
        self.velocity = Vector2(0, -4*4)
        maker = BitmapMaker.instance()

    def interact_with(self, other, fleets):
        other.interact_with_playershot(self, fleets)

    def interact_with_topbumper(self, top_bumper, fleets):
        if top_bumper.intersecting(self.position):
            fleets.remove(self)

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderfleet(self, bumper, fleets):
        pass

    def interact_with_invaderplayer(self, bumper, fleets):
        pass

    def interact_with_playershot(self, bumper, fleets):
        pass

    def draw(self, screen):
        center = self.position
        rect = pygame.Rect(0, 0, 4, 32)
        rect.center = center
        pygame.draw.rect(screen, "white", rect)

    def tick(self, delta_time, fleets):
        pass

    def update(self, delta_time, fleets):
        self.position += self.velocity