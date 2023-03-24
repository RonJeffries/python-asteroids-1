import pygame

vector2 = pygame.Vector2


class Ship():
    def __init__(self, position):
        self.position = position
        self.raw_points = [vector2(-3.0, -2.0), vector2(-3.0, 2.0), vector2(-5.0, 4.0),
                      vector2(7.0, 0.0), vector2(-5.0, -4.0), vector2(-3.0, -2.0)]
        self.raw_flare = [vector2(-3.0, -2.0), vector2(-7.0, 0.0), vector2(-3.0, 2.0)]

    def adjust(self, point):
        return point + vector2(7, 4) + self.position

    def draw(self, screen):
        ship_points = list(map(self.adjust, self.raw_points))
        pygame.draw.lines(screen, "white", False, ship_points)
