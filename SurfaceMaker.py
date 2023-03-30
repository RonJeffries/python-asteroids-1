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

    @staticmethod
    def adjust(point, center_adjustment, scale_factor):
        return (point + center_adjustment) * scale_factor

    @staticmethod
    def ship_surfaces():
        ship_surface = SurfaceMaker.create_scaled_surface((60, 36), Vector2(7, 4), 4, raw_ship_points)
        accelerating_surface = SurfaceMaker.create_scaled_surface((60, 36), Vector2(7, 4), 4, raw_ship_points, raw_flare_points)
        return ship_surface, accelerating_surface

    @staticmethod
    def asteroid_surface(size):
        shape = random.randint(0, 3)
        scale = [4, 8, 16][clamp(size, 0, 2)]
        room_for_fat_line = 1
        surface_size = [32, 64, 128][clamp(size, 0, 2)] + room_for_fat_line
        surface = SurfaceMaker.create_scaled_surface((surface_size, surface_size), Vector2(4, 4), scale, raw_rocks[shape])
        x, y = surface.get_size()
        # pygame.draw.circle(surface, "red", (x/2, y/2),  3)
        return surface

    @staticmethod
    def create_scaled_surface(dimensions, offset, scale, *point_lists):
        surface = pygame.Surface(dimensions)
        surface.set_colorkey((0, 0, 0))
        for point_list in point_lists:
            adjusted = [SurfaceMaker.adjust(point, offset, scale) for point in point_list]
            pygame.draw.lines(surface, "white", False, adjusted, 3)
        return surface
