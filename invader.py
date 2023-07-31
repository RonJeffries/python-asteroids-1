import pygame.draw


class Invader:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen, start, step):
        pos = (start.x+self.x*step, start.y - step*self.y)
        pygame.draw.circle(screen, "red", pos, 16)