import pygame

from invaders.bitmap_maker import BitmapMaker
from flyer import InvadersFlyer


class InvadersExplosion(InvadersFlyer):

    @classmethod
    def saucer_explosion(cls, position, time):
        maker = BitmapMaker()
        image = maker.saucers[1]
        return cls(image, position, time)

    @classmethod
    def shot_explosion(cls, position, time):
        maker = BitmapMaker()
        image = maker.player_shot_explosion
        return cls(image, position, time)

    def __init__(self, image, position, time):
        self.image = image
        self.position = position
        self._mask = pygame.mask.from_surface(image)
        self._rect = image.get_rect()
        self._time = time

    @property
    def mask(self):
        return self._mask

    @property
    def rect(self):
        return self._rect

    def tick(self, delta_time, fleets):
        self._time -= delta_time
        if self._time < 0:
            fleets.remove(self)

    def draw(self, screen):
        self.rect.center = self.position
        screen.blit(self.image, self.rect)

    def interact_with(self, other, fleets):
        other.interact_with_invadersexplosion(self, fleets)
