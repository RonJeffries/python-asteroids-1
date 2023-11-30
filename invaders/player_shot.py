from flyer import InvadersFlyer
from invaders.Collider import Collider
from invaders.bitmap_maker import BitmapMaker
from invaders.shot_explosion import InvadersExplosion
from pygame import Vector2
import pygame
import u
from invaders.sprite import Sprite


class PlayerShot(InvadersFlyer):
    def __init__(self, position=u.CENTER):
        offset = Vector2(2, -8*4)
        self.velocity = Vector2(0, -4*4)
        maker = BitmapMaker.instance()
        bits = maker.player_shot
        self._sprite = Sprite([bits])
        self.position = position + offset
        self.should_die = False
        explosion = BitmapMaker.instance().player_shot_explosion
        self.explosion_mask = pygame.mask.from_surface(explosion)

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

    def hit_invader(self, fleets):
        fleets.remove(self)

    def interact_with(self, other, fleets):
        other.interact_with_playershot(self, fleets)

    def interact_with_invadershot(self, shot, fleets):
        if self.colliding(shot):
            self.explode(fleets)

    def explode(self, fleets):
        fleets.append(InvadersExplosion.shot_explosion(self.position, 0.125))
        fleets.remove(self)

    def interact_with_invaderssaucer(self, saucer, fleets):
        if self.colliding(saucer):
            fleets.remove(self)

    def interact_with_roadfurniture(self, shield, fleets):
        if self.colliding(shield):
            fleets.remove(self)

    def interact_with_topbumper(self, top_bumper, fleets):
        if top_bumper.intersecting(self.position):
            self.explode(fleets)

    def colliding(self, invaders_flyer):
        collider = Collider(self, invaders_flyer)
        return collider.colliding()

    def draw(self, screen):
        self._sprite.draw(screen)

    def update(self, delta_time, fleets):
        self.position = self.position + self.velocity
