import pygame

from invaders.bitmap_maker import BitmapMaker
from flyer import InvadersFlyer


class InvaderExplosion(InvadersFlyer):
    def __init__(self, position):
        self.position = position
        maker = BitmapMaker()
        self.image = maker.invader_explosion
        self._mask = pygame.mask.from_surface(self.image)
        self._rect = self.image.get_rect()
        # self.image.fill("red",self.rect, special_flags=pygame.BLEND_MULT)
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

    def interact_with(self, other, fleets):
        other.interact_with_invaderexplosion(self, fleets)