import pygame.draw
from pygame import Vector2

import u
from invaders.Collider import Collider
from invaders.invader_explosion import InvaderExplosion
from invaders.invader_score import InvaderScore
from sounds import player

INVADER_SPACING = 64


class Invader:
    def __init__(self, column, row, bitmaps):
        self._score = [10, 10, 20, 20, 30][row]
        self.bitmaps = bitmaps
        self.masks = [pygame.mask.from_surface(bitmap) for bitmap in self.bitmaps]
        self.column = column
        self.relative_position = Vector2(INVADER_SPACING * column, -INVADER_SPACING * row)
        self.rect = pygame.Rect(0, 0, 64, 32)
        self.image = 0

    @property
    def mask(self):
        return self.masks[self.image]

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

    @property
    def position(self):
        return Vector2(self.rect.center)

    @position.setter
    def position(self, vector):
        self.image = 1 if self.image == 0 else 0
        self.rect.center = vector + self.relative_position

    def draw(self, screen):
        if screen:
            screen.blit(self.bitmaps[self.image], self.rect)
            # circle_color = "green" if self.relative_position == Vector2(0, 0) else "red"
            # pygame.draw.rect(screen, "yellow", self.rect)
            # pygame.draw.circle(screen, circle_color, self.rect.center, 16)

    def interact_with_bumper(self, bumper, invader_group, current_direction):
        if bumper.intersecting(self.rect) and bumper.incoming_direction == current_direction:
            invader_group.at_edge(bumper.incoming_direction)

    def x_fraction(self):
        x = self.rect.centerx - u.BUMPER_LEFT
        denom = u.BUMPER_RIGHT - u.BUMPER_LEFT
        return x / denom
