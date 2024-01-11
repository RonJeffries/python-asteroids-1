from flyer import InvadersFlyer
from invaders.bitmap_maker import BitmapMaker
from invaders.exploder import Exploder
from invaders.generic_explosion import GenericExplosion
from pygame import Vector2
import pygame
import u
from invaders.sprite import Sprite, SpritelyMixin


class PlayerShot(SpritelyMixin, InvadersFlyer):
    def __init__(self, position=u.CENTER):
        offset = Vector2(2, -8*4)
        self.velocity = Vector2(0, -4*4)
        self._sprite = Sprite.player_shot()
        self.position = position + offset
        self.should_die = False
        explosion = BitmapMaker.instance().player_shot_explosion
        self.explosion_mask = pygame.mask.from_surface(explosion)

    def hit_invader(self, _invader, fleets):
        fleets.remove(self)

    def interact_with(self, other, fleets):
        other.interact_with_playershot(self, fleets)

    def interact_with_invadershot(self, shot, fleets):
        if self.colliding(shot):
            self.explode(fleets)

    def explode(self, fleets):
        Exploder.explode_player_shot(self.position, fleets)
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

    def update(self, delta_time, fleets):
        self.position = self.position + self.velocity
