import pygame.draw
from pygame import Vector2

INVADER_SPACING = 64


class Invader:
    def __init__(self, row, column):
        self.relative_position = Vector2(INVADER_SPACING * row, INVADER_SPACING * column)
        self.rect = pygame.Rect(0, 0, 64, 32)

    @property
    def position(self):
        return Vector2(self.rect.center)

    def set_position(self, origin):
        pos = origin + self.relative_position
        self.rect.center = pos

    def draw(self, screen):
        if screen:
            pygame.draw.rect(screen, "yellow", self.rect)
            pygame.draw.circle(screen, "red", self.rect.center, 16)

    def interact_with_bumper(self, bumper, invader_fleet):
        if bumper.intersecting(self.rect):
            invader_fleet.at_edge(bumper.incoming_direction)