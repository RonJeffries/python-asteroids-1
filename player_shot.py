import pygame
from pygame import Vector2

import u
from bitmap_maker import BitmapMaker
from flyer import InvadersFlyer


class ShotExplosion(InvadersFlyer):
    def __init__(self, position):
        self.position = position
        maker = BitmapMaker()
        self.image = maker.player_shot_explosion
        self.rect = self.image.get_rect()
        self.image.fill("red",self.rect, special_flags=pygame.BLEND_MULT)
        self.time = 0.125

    def tick(self, delta_time, fleets):
        self.time -= delta_time
        if self.time < 0:
            fleets.remove(self)

    def draw(self, screen):
        self.rect.center = self.position
        screen.blit(self.image, self.rect)

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderfleet(self, bumper, fleets):
        pass

    def interact_with_invaderplayer(self, bumper, fleets):
        pass

    def interact_with_playershot(self, bumper, fleets):
        pass

    def interact_with(self, other, fleets):
        pass

class PlayerShot(InvadersFlyer):
    def __init__(self, position=u.CENTER):
        offset = Vector2(2, -8*4)
        self.position = position + offset
        self.velocity = Vector2(0, -4*4)
        maker = BitmapMaker.instance()
        self.bits = maker.player_shot
        self.rect = self.bits.get_rect()

    def interact_with(self, other, fleets):
        other.interact_with_playershot(self, fleets)

    def interact_with_topbumper(self, top_bumper, fleets):
        if top_bumper.intersecting(self.position):
            fleets.remove(self)
            fleets.append(ShotExplosion(self.position))

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderfleet(self, bumper, fleets):
        pass

    def interact_with_invaderplayer(self, bumper, fleets):
        pass

    def interact_with_playershot(self, bumper, fleets):
        pass

    def draw(self, screen):
        self.rect.center = self.position
        screen.blit(self.bits, self.rect)

    def tick(self, delta_time, fleets):
        pass

    def update(self, delta_time, fleets):
        self.position += self.velocity
