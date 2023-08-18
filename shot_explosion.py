import pygame

from bitmap_maker import BitmapMaker
from flyer import InvadersFlyer


class ShotExplosion(InvadersFlyer):

    def __init__(self, position):
        self.position = position
        maker = BitmapMaker()
        self.image = maker.player_shot_explosion
        self._mask = pygame.mask.from_surface(self.image)
        self._rect = self.image.get_rect()
        self.image.fill("red",self.rect, special_flags=pygame.BLEND_MULT)
        self.time = 0.125

    @property
    def mask(self):
        return self._mask

    @property
    def rect(self):
        return self._rect

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

    def interact_with_invadershot(self, shot, fleets):
        pass

    def interact_with_playerexplosion(self, _explosion, _fleets):
        pass

    def interact_with_playershot(self, bumper, fleets):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_playerexplosion(self, fleets)
