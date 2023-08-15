import pygame.draw
from pygame import Vector2

INVADER_SPACING = 64


class Invader:
    def __init__(self, column, row, bitmaps):
        self.bitmaps = bitmaps
        self.masks = [pygame.mask.from_surface(bitmap) for bitmap in self.bitmaps]
        self.column = column
        self.relative_position = Vector2(INVADER_SPACING * column, -INVADER_SPACING * row)
        self.rect = pygame.Rect(0, 0, 64, 32)
        self.image = 0

    @property
    def mask(self):
        return self.masks[self.image]

    def mask_offset(self, invaders_flyer):
        return Vector2(invaders_flyer.rect.topleft) - Vector2(self.rect.topleft)

    def masks_overlap(self, invaders_flyer):
        return self.mask.overlap(invaders_flyer.mask, self.mask_offset(invaders_flyer))

    def colliding(self, invaders_flyer):
        return self.rectangles_overlap(invaders_flyer) and self.masks_overlap(invaders_flyer)

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

    def interact_with_bumper(self, bumper, invader_fleet):
        if bumper.intersecting(self.rect):
            invader_fleet.at_edge(bumper.incoming_direction)

    def rectangles_overlap(self, shot):
        return self.rect.colliderect(shot.rect)
