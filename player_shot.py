import pygame
from pygame import Vector2

import u
from Collider import Collider
from bitmap_maker import BitmapMaker
from flyer import InvadersFlyer
from shot_explosion import ShotExplosion


class PlayerShot(InvadersFlyer):
    def __init__(self, position=u.CENTER):
        offset = Vector2(2, -8*4)
        self.velocity = Vector2(0, -4*4)
        maker = BitmapMaker.instance()
        self.bits = maker.player_shot
        self._mask = pygame.mask.from_surface(self.bits)
        self._rect = self.bits.get_rect()
        self.position = position + offset
        self.should_die = False

    @property
    def mask(self):
        return self._mask

    @property
    def rect(self):
        return self._rect

    def begin_interactions(self, fleets):
        self.should_die = False

    def hit_invader(self):
        self.should_die = True

    def end_interactions(self, fleets):
        if self.should_die:
            fleets.remove(self)

    @property
    def position(self):
        return Vector2(self.rect.center)

    @position.setter
    def position(self, vector):
        self.rect.center = vector

    def interact_with(self, other, fleets):
        other.interact_with_playershot(self, fleets)

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_topbumper(self, top_bumper, fleets):
        if top_bumper.intersecting(self.position):
            fleets.remove(self)
            fleets.append(ShotExplosion(self.position))

    def interact_with_invaderfleet(self, bumper, fleets):
        pass

    def interact_with_invaderplayer(self, bumper, fleets):
        pass

    def interact_with_invadershot(self, shot, fleets):
        if self.colliding(shot):
            fleets.remove(self)
            fleets.append(ShotExplosion(self.position))

    def colliding(self, invaders_flyer):
        collider = Collider(self, invaders_flyer)
        return collider.colliding()

    def interact_with_playerexplosion(self, _explosion, _fleets):
        pass

    def interact_with_playershot(self, bumper, fleets):
        pass

    def draw(self, screen):
        self.rect.center = self.position
        screen.blit(self.bits, self.rect)

    def tick(self, delta_time, fleets):
        pass

    def update(self, delta_time, fleets):
        self.position = self.position + self.velocity
