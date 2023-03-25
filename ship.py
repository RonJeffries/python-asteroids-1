import pygame
import random

vector2 = pygame.Vector2


class Ship:
    def __init__(self, position):
        self.position = position
        self.angle = 0
        self.accelerating = True
        self.raw_ship = [vector2(-3.0, -2.0), vector2(-3.0, 2.0), vector2(-5.0, 4.0),
                         vector2(7.0, 0.0), vector2(-5.0, -4.0), vector2(-3.0, -2.0)]
        self.raw_flare = [vector2(-3.0, -2.0), vector2(-7.0, 0.0), vector2(-3.0, 2.0)]
        self.ship_surface = pygame.Surface((60, 36))
        self.ship_surface.set_colorkey((0, 0, 0))
        self.ship_accelerating_surface = pygame.Surface((60, 36))
        self.ship_accelerating_surface.set_colorkey((0, 0, 0))
        self.paint()

    def adjust(self, point):
        return point*4 + vector2(28, 16)

    def draw(self, screen):
        ship_source = self.select_ship_source()
        copy = pygame.transform.rotate(ship_source.copy(), self.angle)
        half = pygame.Vector2(copy.get_size())/2
        screen.blit(copy, self.position - half)

    def select_ship_source(self):
        if self.accelerating and random.random() >= 0.66:
            return self.ship_accelerating_surface
        else:
            return self.ship_surface

    def paint(self):
        ship_points = list(map(self.adjust, self.raw_ship))
        flare_points = list(map(self.adjust, self.raw_flare))
        pygame.draw.lines(self.ship_surface, "white", False, ship_points, 3)
        pygame.draw.lines(self.ship_accelerating_surface, "white", False, ship_points, 3)
        pygame.draw.lines(self.ship_accelerating_surface, "white", False, flare_points, 3)
