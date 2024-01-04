import pygame.draw
from pygame import Vector2, Mask

import u
from invaders.generic_explosion import GenericExplosion
from invaders.invader_score import InvaderScore
from invaders.sprite import Sprite, SpritelyMixin
from sounds import player


class Invader(SpritelyMixin):
    def __init__(self, column, row, sprite):
        self._score = [10, 10, 20, 20, 30][row]
        self._sprite = sprite
        self.column = column
        self.relative_position = Vector2(u.INVADER_SPACING * column, -u.INVADER_SPACING * row)
        self.image = 0

    @property
    def explosion_mask(self):
        return self.sprite.mask

    def move_relative_to(self, vector):
        self._sprite.next_frame()
        self.position = vector + self.relative_position

    def interact_with_group_and_playershot(self, shot, group, fleets):
        if self.colliding(shot):
            player.play_stereo("invaderkilled", u.screen_fraction(self.position))
            shot.hit_invader(self, fleets)
            group.kill(self)
            fleets.append(InvaderScore(self._score))
            explosion = GenericExplosion.invader_explosion(self.position, 0.125)
            fleets.append(explosion)

    def interact_with_invaderplayer(self, player, fleets):
        if self.colliding(player):
            player.hit_invader(self, fleets)

    def interact_with_roadfurniture(self, shield, fleets):
        if self.colliding(shield):
            shield.hit_invader(self, fleets)

    def is_out_of_bounds(self, low, high):
        return self.position.x < low or self.position.x > high
