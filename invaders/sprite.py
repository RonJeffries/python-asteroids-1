import pygame
from pygame import Vector2, Rect

from invaders.ImageMasher import ImageMasher
from invaders.bitmap_maker import BitmapMaker


class Sprite:
    def __init__(self, surfaces):
        self._surfaces = surfaces
        self._masks = [pygame.mask.from_surface(surface) for surface in self._surfaces]
        self._rectangle = self._surfaces[0].get_rect()
        self._frame_number = 0

    @classmethod
    def squiggles(cls):
        return cls(BitmapMaker.instance().squiggles)

    @classmethod
    def rollers(cls):
        return cls(BitmapMaker.instance().rollers)

    @classmethod
    def plungers(cls):
        return cls(BitmapMaker.instance().plungers)

    @classmethod
    def shield(cls):
        surface = BitmapMaker.instance().shield.copy()
        surface.set_colorkey("black")
        return cls((surface,))

    @classmethod
    def player(cls):
        return cls((BitmapMaker.instance().players[0], ))

    @classmethod
    def saucer(cls):
        return cls((BitmapMaker.instance().saucer, ))

    @classmethod
    def player_shot(cls):
        return cls((BitmapMaker.instance().player_shot, ))

    @classmethod
    def invader(cls, row):
        start, end = ((0, 2), (0, 2), (2, 4), (2, 4), (4, 6))[row]
        maps = BitmapMaker.instance().invaders
        return Sprite(maps[start:end])

    @property
    def mask(self):
        return self._masks[self._frame_number]

    @property
    def position(self):
        return Vector2(self.rectangle.center)

    @position.setter
    def position(self, value):
        self.rectangle.center = value

    @property
    def rectangle(self):
        return self._rectangle

    @property
    def surface(self):
        return self._surfaces[self._frame_number]

    def colliding(self, other):
        return self.rectangles_collide(other) and self.masks_collide(other)

    def rectangles_collide(self, other):
        return self.rectangle.colliderect(other.rectangle)

    def masks_collide(self, other):
        return self.mask.overlap(other.mask, self.offset(other))

    def offset(self, other):
        return Vector2(other.rectangle.topleft) - Vector2(self.rectangle.topleft)

    def next_frame(self):
        self._frame_number = (self._frame_number + 1) % len(self._surfaces)

    def draw(self, screen):
        screen.blit(self.surface, self.rectangle)

    def mash_from(self, shot):
        masher = ImageMasher.from_flyers(self, shot)
        new_mask, new_surface = masher.update(self.surface)
        self._masks = (new_mask,)
        self._surfaces = (new_surface,)

    def colliding_with_flyer(self, flyer):
        return self.colliding(flyer._sprite)


class Spritely:
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