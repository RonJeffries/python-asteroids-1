import pygame.draw
from pygame import Vector2


class Invader:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.rect = pygame.Rect(0, 0, 64, 32)

    @property
    def position(self):
        return Vector2(self.rect.center)

    def move_relative(self, origin):
        pos = Vector2(origin.x + 64*self.row, origin.y - 64*self.column)
        self.rect.center = pos

    def draw(self, screen):
        if screen:
            pygame.draw.rect(screen, "yellow", self.rect)
            pygame.draw.circle(screen, "red", self.rect.center, 16)

    def interact_with_bumper(self, bumper, invader_fleet):
        if bumper.intersecting(self.rect):
            invader_fleet.at_edge(bumper.incoming_direction)