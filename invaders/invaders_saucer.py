import pygame
from pygame import Vector2
import u
from flyer import InvadersFlyer
from invaders.bitmap_maker import BitmapMaker


class InvadersSaucer(InvadersFlyer):
    def __init__(self, direction=1):
        self.direction = direction
        maker = BitmapMaker.instance()
        self.saucers = maker.saucers  # one turret, two explosions
        self._map = self.saucers[0]
        self._mask = pygame.mask.from_surface(self._map)
        self._rect = self._map.get_rect()
        self.left = 64
        self.rect.center = Vector2(self.left, u.INVADER_SAUCER_Y)

    @property
    def mask(self):
        return self._mask

    @property
    def rect(self):
        return self._rect

    @property
    def position(self):
        return Vector2(self.rect.center)

    @position.setter
    def position(self, value):
        self.rect.center = value

    def interact_with(self, other, fleets):
        other.interact_with_invaderssaucer(self, fleets)

    def update(self, delta_time, fleets):
        x = self.position.x + 16
        x_max = 960
        if x > x_max:
            fleets.remove(self)
        else:
            self.position = (x, self.position.y)

    def draw(self, screen):
        screen.blit(self._map, self.rect)


class InvadersSaucerMaker:
    pass
