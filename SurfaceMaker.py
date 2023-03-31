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

    next_shape = 0

    @staticmethod
    def adjust(point, center_adjustment, scale_factor):
        return (point + center_adjustment) * scale_factor

    @staticmethod
    def ship_surfaces():
        ship_surface = SurfaceMaker.create_scaled_surface((60, 36), Vector2(7, 4), 4, raw_ship_points)
        accelerating_surface = SurfaceMaker.create_scaled_surface((60, 36), Vector2(7, 4), 4, raw_ship_points, raw_flare_points)
        return ship_surface, accelerating_surface

    @staticmethod
    def asteroid_surface(actual_size):
        shape = SurfaceMaker.next_shape
        SurfaceMaker.next_shape = (SurfaceMaker.next_shape + 1) % 4
        scale = actual_size/8
        room_for_fat_line = 2
        surface_size = actual_size + room_for_fat_line
        offset = Vector2(4, 4)
        surface = SurfaceMaker.create_scaled_surface((surface_size, surface_size), offset, scale, raw_rocks[shape])
        return surface

    @staticmethod
    def create_scaled_surface(dimensions, offset, scale_factor, *point_lists):
        surface = pygame.Surface(dimensions)
        surface.set_colorkey((0, 0, 0))
        for point_list in point_lists:
            adjusted = [SurfaceMaker.adjust(point, offset, scale_factor) for point in point_list]
            pygame.draw.lines(surface, "white", False, adjusted, 3)
        return surface
