import pygame
from pygame import Vector2
import u
from flyer import InvadersFlyer
from invaders.bitmap_maker import BitmapMaker
from invaders.timecapsule import TimeCapsule


class InvadersSaucer(InvadersFlyer):
    def __init__(self, direction=1):
        self.direction = direction
        maker = BitmapMaker.instance()
        self.saucers = maker.saucers  # one turret, two explosions
        self._map = self.saucers[0]
        self._mask = pygame.mask.from_surface(self._map)
        self._rect = self._map.get_rect()
        half_width = self._rect.width // 2
        self._left = u.BUMPER_LEFT + half_width
        self._right = u.BUMPER_RIGHT - half_width
        self.rect.center = Vector2(self._left, u.INVADER_SAUCER_Y)
        self._speed = 8

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

    def interact_with_invaderfleet(self, invader_fleet, fleets):
        if invader_fleet.invader_count() < 8:
            self.die(fleets)

    def die(self, fleets):
        fleets.remove(self)
        fleets.append(TimeCapsule(10, InvadersSaucer()))

    def update(self, delta_time, fleets):
        x = self.position.x + self._speed
        if x > self._right:
            self.die(fleets)
        else:
            self.position = (x, self.position.y)

    def draw(self, screen):
        screen.blit(self._map, self.rect)

