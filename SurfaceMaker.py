import pygame
from pygame import Vector2

raw_rocks = [
    [
        Vector2(4.0, 2.0), Vector2(3.0, 0.0), Vector2(4.0, -2.0),
        Vector2(1.0, -4.0), Vector2(-2.0, -4.0), Vector2(-4.0, -2.0),
        Vector2(-4.0, 2.0), Vector2(-2.0, 4.0), Vector2(0.0, 2.0),
        Vector2(2.0, 4.0), Vector2(4.0, 2.0),
    ],
    [
        Vector2(2.0, 1.0), Vector2(4.0, 2.0), Vector2(2.0, 4.0),
        Vector2(0.0, 3.0), Vector2(-2.0, 4.0), Vector2(-4.0, 2.0),
        Vector2(-3.0, 0.0), Vector2(-4.0, -2.0), Vector2(-2.0, -4.0),
        Vector2(-1.0, -3.0), Vector2(2.0, -4.0), Vector2(4.0, -1.0),
        Vector2(2.0, 1.0)
    ],
    [
        Vector2(-2.0, 0.0), Vector2(-4.0, -1.0), Vector2(-2.0, -4.0),
        Vector2(0.0, -1.0), Vector2(0.0, -4.0), Vector2(2.0, -4.0),
        Vector2(4.0, -1.0), Vector2(4.0, 1.0), Vector2(2.0, 4.0),
        Vector2(-1.0, 4.0), Vector2(-4.0, 1.0), Vector2(-2.0, 0.0)
    ],
    [
        Vector2(1.0, 0.0), Vector2(4.0, 1.0), Vector2(4.0, 2.0),
        Vector2(1.0, 4.0), Vector2(-2.0, 4.0), Vector2(-1.0, 2.0),
        Vector2(-4.0, 2.0), Vector2(-4.0, -1.0), Vector2(-2.0, -4.0),
        Vector2(1.0, -3.0), Vector2(2.0, -4.0), Vector2(4.0, -2.0),
        Vector2(1.0, 0.0)
    ]
]


class SurfaceMaker:
    def __init__(self):
        self._two = 2
        pass

    def adjust(self, point, center_adjustment, scale_factor):
        return (point + center_adjustment) * scale_factor

    def get_ship_points(self):
        ship_points = [Vector2(-3.0, -2.0), Vector2(-3.0, 2.0), Vector2(-5.0, 4.0),
                       Vector2(7.0, 0.0), Vector2(-5.0, -4.0), Vector2(-3.0, -2.0)]
        return [self.adjust(point, Vector2(7, 4), 4) for point in ship_points]

    def get_flare_points(self):
        flare_points = [Vector2(-3.0, -2.0), Vector2(-7.0, 0.0), Vector2(-3.0, 2.0)]
        return [self.adjust(point, Vector2(7, 4), 4) for point in flare_points]

    def make_ship_surface(self, ship_points):
        ship_surface = pygame.Surface((60, 36))
        ship_surface.set_colorkey((0, 0, 0))
        pygame.draw.lines(ship_surface, "white", False, ship_points, 3)
        return ship_surface

    def make_accelerating_surface(self, flare_points, ship_points):
        ship_accelerating_surface = self.make_ship_surface(ship_points)
        pygame.draw.lines(ship_accelerating_surface, "white", False, flare_points, 3)
        return ship_accelerating_surface

    def prepare_surfaces(self):
        ship_points = self.get_ship_points()
        flare_points = self.get_flare_points()
        return (self.make_ship_surface(ship_points)), (self.make_accelerating_surface(flare_points, ship_points))

    def asteroid_surface(self, shape, size):
        surface = pygame.Surface((128, 128))
        surface.set_colorkey((0, 0, 0))
        adjusted = [self.adjust(point, Vector2(4, 4), 16) for point in raw_rocks[1]]
        pygame.draw.lines(surface, "white", False, adjusted, 3)
        return surface
