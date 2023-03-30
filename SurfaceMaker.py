import random

import pygame
from pygame import Vector2
from pygame.math import clamp

raw_ship_points = [Vector2(-3.0, -2.0), Vector2(-3.0, 2.0), Vector2(-5.0, 4.0),
                   Vector2(7.0, 0.0), Vector2(-5.0, -4.0), Vector2(-3.0, -2.0)]
raw_flare_points = [Vector2(-3.0, -2.0), Vector2(-7.0, 0.0), Vector2(-3.0, 2.0)]

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
        pass

    def adjust(self, point, center_adjustment, scale_factor):
        return (point + center_adjustment) * scale_factor

    def ship_surfaces(self):
        ship_surface = self.create_scaled_surface((60, 36), Vector2(7, 4), 4, raw_ship_points)
        accelerating_surface = self.create_scaled_surface((60, 36), Vector2(7, 4), 4, raw_ship_points, raw_flare_points)
        return ship_surface, accelerating_surface

    def asteroid_surface(self, size):
        shape = random.randint(0,3)
        scale = [4, 8, 16][clamp(size, 0, 3)]
        return self.create_scaled_surface((128, 128), Vector2(4, 4), scale, raw_rocks[shape])

    def create_scaled_surface(self, dimensions, offset, scale, *point_lists):
        surface = pygame.Surface(dimensions)
        surface.set_colorkey((0, 0, 0))
        for point_list in point_lists:
            adjusted = [self.adjust(point, offset, scale) for point in point_list]
            pygame.draw.lines(surface, "white", False, adjusted, 3)
        return surface
