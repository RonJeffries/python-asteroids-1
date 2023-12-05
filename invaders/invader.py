import pygame.draw
from pygame import Vector2

import u
from invaders.Collider import Collider
from invaders.invader_explosion import InvaderExplosion
from invaders.invader_score import InvaderScore
from invaders.sprite import Sprite, Spritely
from sounds import player

INVADER_SPACING = 64


class Invader(Spritely):
    def __init__(self, column, row, sprite):
        self._score = [10, 10, 20, 20, 30][row]
        self._sprite = sprite
        self.column = column
        self.relative_position = Vector2(INVADER_SPACING * column, -INVADER_SPACING * row)
        self.image = 0

    def move_relative_to(self, vector):
        self._sprite.next_frame()
        self.position = vector + self.relative_position

    def interact_with_group_and_playershot(self, shot, group, fleets):
        if self.colliding(shot):
            player.play_stereo("invaderkilled", self.x_fraction())
            shot.hit_invader(fleets)
            group.kill(self)
            fleets.append(InvaderScore(self._score))
            fleets.append(InvaderExplosion(self.position))

    def colliding(self, invaders_flyer):
        collider = Collider(self, invaders_flyer)
        return collider.colliding()

    def is_entering(self, bumper, current_direction):
        return bumper.am_i_entering(self.rect, current_direction)

    def x_fraction(self):
        x_distance = self.rect.centerx - u.BUMPER_LEFT
        total_distance = u.BUMPER_RIGHT - u.BUMPER_LEFT
        return x_distance / total_distance
