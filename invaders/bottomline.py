
from flyer import InvadersFlyer
from pygame import Rect, Surface
import pygame.draw_py
import u


class BottomLine(InvadersFlyer):
    def __init__(self):
        w = 960-128
        h = 4
        surface = Surface((w, h))
        surface.set_colorkey((0, 0, 0))
        surface.fill("green")
        rect = Rect(0, 0, w, h)
        rect.bottomleft = (64, u.SCREEN_SIZE - 56)
        self._rect = rect
        self.map = surface
        self._mask = pygame.mask.from_surface(surface)

    @property
    def mask(self):
        return self._mask

    @property
    def rect(self):
        return self._rect

    def draw(self, screen):
        screen.blit(self.map, self.rect)

    def interact_with(self, other, fleets):
        other.interact_with_bottomline(self, fleets)

