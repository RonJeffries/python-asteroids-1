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
        explosion = BitmapMaker.instance().player_shot_explosion
        self.explosion_mask = pygame.mask.from_surface(explosion)

    @property
    def mask(self):
        return self._mask

    @property
    def rect(self):
        return self._rect

    def begin_interactions(self, fleets):
        pass

    def hit_invader(self, fleets):
        fleets.remove(self)

    def end_interactions(self, fleets):
        pass

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

    def interact_with_invaderexplosion(self, explosion, fleets):
        pass

    def interact_with_invaderfleet(self, bumper, fleets):
        pass

    def interact_with_invaderplayer(self, bumper, fleets):
        pass

    def interact_with_invadershot(self, shot, fleets):
        if self.colliding(shot):
            fleets.append(ShotExplosion(self.position))
            fleets.remove(self)

    def interact_with_playerexplosion(self, _explosion, _fleets):
        pass

    def interact_with_playershot(self, bumper, fleets):
        pass

    def interact_with_shield(self, shield, fleets):
        if self.colliding(shield):
            fleets.remove(self)

    def interact_with_shotcontroller(self, controller, fleets):
        pass

    def interact_with_shotexplosion(self, bumper, fleets):
        pass

    def interact_with_topbumper(self, top_bumper, fleets):
        if top_bumper.intersecting(self.position):
            fleets.append(ShotExplosion(self.position))
            fleets.remove(self)

    def colliding(self, invaders_flyer):
        collider = Collider(self, invaders_flyer)
        return collider.colliding()

    def draw(self, screen):
        self.rect.center = self.position
        screen.blit(self.bits, self.rect)

    def tick(self, delta_time, fleets):
        pass

    def update(self, delta_time, fleets):
        self.position = self.position + self.velocity
