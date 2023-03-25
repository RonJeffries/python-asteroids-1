import pygame
import random

vector2 = pygame.Vector2


class Ship:
    def __init__(self, position):
        self.position = position
        self.angle = 0
        self.accelerating = False
        self.raw_points = [vector2(-3.0, -2.0), vector2(-3.0, 2.0), vector2(-5.0, 4.0),
                           vector2(7.0, 0.0), vector2(-5.0, -4.0), vector2(-3.0, -2.0)]
        self.raw_flare = [vector2(-3.0, -2.0), vector2(-7.0, 0.0), vector2(-3.0, 2.0)]
        self.surface = pygame.Surface((60, 36))
        self.surface.set_colorkey((0, 0, 0))
        self.flare_surface = pygame.Surface((60, 36))
        self.flare_surface.set_colorkey((0, 0, 0))
        self.paint(self.surface, self.flare_surface)

    def adjust(self, point):
        return point*4 + vector2(28, 16)

    def draw(self, screen):
        if not self.accelerating or random.random() < 0.66:
            ship_source = self.surface
        else:
            ship_source = self.flare_surface
        copy = pygame.transform.rotate(ship_source.copy(), self.angle)
        half = pygame.Vector2(copy.get_size())/2
        screen.blit(copy, self.position - half)

    def paint(self, surface, flare_surface):
        ship_points = list(map(self.adjust, self.raw_points))
        flare_points = list(map(self.adjust, self.raw_flare))
        pygame.draw.lines(surface, "white", False, ship_points, 3)
        pygame.draw.lines(flare_surface, "white", False, ship_points, 3)
        pygame.draw.lines(flare_surface, "white", False, flare_points, 3)
