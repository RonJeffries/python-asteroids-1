from flyer import InvadersFlyer
from invaders.Collider import Collider
from invaders.bitmap_maker import BitmapMaker
from invaders.shot_explosion import ShotExplosion
from pygame import Vector2
import pygame
import u


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

    @property
    def position(self):
        return Vector2(self._rect.center)

    @position.setter
    def position(self, vector):
        self._rect.center = vector

    def begin_interactions(self, fleets):
        pass

    def hit_invader(self, fleets):
        fleets.remove(self)

    def end_interactions(self, fleets):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_playershot(self, fleets)

    def interact_with_invadershot(self, shot, fleets):
        if self.colliding(shot):
            fleets.append(ShotExplosion(self.position))
            fleets.remove(self)

    def interact_with_shield(self, shield, fleets):
        if self.colliding(shield):
            fleets.remove(self)

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

    def update(self, delta_time, fleets):
        self.position = self.position + self.velocity
