import pygame

vector2 = pygame.Vector2


class Ship():
    def __init__(self, position):
        self.position = position
        self.raw_points = [vector2(-3.0, -2.0), vector2(-3.0, 2.0), vector2(-5.0, 4.0),
                           vector2(7.0, 0.0), vector2(-5.0, -4.0), vector2(-3.0, -2.0)]
        self.raw_flare = [vector2(-3.0, -2.0), vector2(-7.0, 0.0), vector2(-3.0, 2.0)]
        self.surface = pygame.Surface((60, 36))
        self.paint(self.surface)

    def adjust(self, point):
        return point*4 + vector2(28, 16)

    def draw(self, screen):
        screen.blit(self.surface, self.position)

    def paint(self, surface):
        ship_points = list(map(self.adjust, self.raw_points))
        pygame.draw.lines(surface, "white", False, ship_points)
