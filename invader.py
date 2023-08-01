import pygame.draw


class Invader:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.rect = pygame.Rect(0, 0, 32, 32)

    def draw(self, screen, start, step):
        pos = (start.x + step*self.row, start.y - step*self.column)
        self.rect.center = pos
        if screen:
            pygame.draw.rect(screen, "yellow", self.rect)
            pygame.draw.circle(screen, "red", pos, 16)

    def interact_with_bumper(self, bumper, invader_fleet):
        if bumper.rect.colliderect(self.rect):
            invader_fleet.at_edge()