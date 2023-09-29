import pygame
from pygame import Surface

import u
from invaders.Collider import Collider
from invaders.ImageMasher import ImageMasher
from invaders.bitmap_maker import BitmapMaker
from flyer import InvadersFlyer
from core.tasks import Tasks


class Shield(InvadersFlyer):
    @classmethod
    def shield(cls, position):
        surface = BitmapMaker.instance().shield
        return cls(surface, position)

    @classmethod
    def bottom_line(cls):
        w = 960-128
        h = 4
        surface = Surface((w, h))
        surface.fill("green")
        rect = surface.get_rect()
        rect.bottomleft = (64, u.SCREEN_SIZE - 56)
        position = rect.center
        return cls(surface, position)

    def __init__(self, surface, position):
        self._map = surface.copy()
        self._map.set_colorkey("black")
        self._mask = pygame.mask.from_surface(surface)
        self._rect = self._map.get_rect()
        self._rect.center = position
        self._tasks = Tasks()

    @property
    def mask(self):
        return self._mask

    @property
    def rect(self):
        return self._rect

    @property
    def position(self):
        return self._rect.center

    def draw(self, screen):
        screen.blit(self._map, self.rect)

    def begin_interactions(self, fleets):
        self._tasks.clear()

    def end_interactions(self, fleets):
        self._tasks.finish()

    def interact_with(self, other, fleets):
        other.interact_with_shield(self, fleets)

    def interact_with_invadershot(self, shot, fleets):
        self.process_shot_collision(shot)

    def interact_with_playershot(self, shot, fleets):
        self.process_shot_collision(shot)

    def process_shot_collision(self, shot):
        if Collider(self, shot).colliding():
            self._tasks.remind_me(lambda: self.mash_image(shot))

    def mash_image(self, shot):
        masher = ImageMasher.from_flyers(self, shot)
        self._mask, self._map = masher.update(self._mask, self._map)

