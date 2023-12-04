import pygame
from pygame import Surface

import u
from invaders.Collider import Collider
from invaders.ImageMasher import ImageMasher
from invaders.bitmap_maker import BitmapMaker
from flyer import InvadersFlyer
from core.tasks import Tasks
from invaders.sprite import Sprite
from u import BOTTOM_LINE_OFFSET


class RoadFurniture(InvadersFlyer):
    @classmethod
    def shield(cls, position):
        sprite = Sprite.shield()
        return cls(sprite, position)

    @classmethod
    def bottom_line(cls):
        w = 960-128
        h = 4
        surface = Surface((w, h))
        surface.fill("green")
        surface.set_colorkey("black")
        rect = surface.get_rect()
        rect.bottomleft = (64, u.SCREEN_SIZE - BOTTOM_LINE_OFFSET)
        position = rect.center
        sprite = Sprite((surface,))
        return cls(sprite, position)

    def __init__(self, sprite, position):
        self._sprite = sprite
        self.position = position
        self._tasks = Tasks()

    @property
    def mask(self):
        return self._sprite.mask

    @property
    def rect(self):
        return self._sprite.rectangle

    @property
    def position(self):
        return self._sprite.position

    @position.setter
    def position(self, vector):
        self._sprite.position = vector

    def draw(self, screen):
        self._sprite.draw(screen)

    def begin_interactions(self, fleets):
        self._tasks.clear()

    def end_interactions(self, fleets):
        self._tasks.finish()

    def interact_with(self, other, fleets):
        other.interact_with_roadfurniture(self, fleets)

    def interact_with_invadershot(self, shot, fleets):
        self.process_shot_collision(shot)

    def interact_with_playershot(self, shot, fleets):
        self.process_shot_collision(shot)

    def process_shot_collision(self, shot):
        if Collider(self, shot).colliding():
            self._tasks.remind_me(lambda: self.mash_image(shot))

    def mash_image(self, shot):
        masher = ImageMasher.from_flyers(self, shot)
        new_mask, new_surface = masher.update(self.mask, self.surface)
        self._sprite._masks = (new_mask,)
        self._sprite._surfaces = (new_surface,)

    # noinspection PyProtectedMember
    @property
    def surface(self):
        return self._sprite._surfaces[0]

