# SurfaceMaker

import pygame
from pygame import Vector2

raw_saucer_points = [
    Vector2(-2.0, -1.0), Vector2(2.0, -1.0), Vector2(5.0, 1.0),
    Vector2(-5.0, 1.0), Vector2(-2.0, 3.0), Vector2(2.0, 3.0),
    Vector2(5.0, 1.0), Vector2(2.0, -1.0), Vector2(1.0, -3.0),
    Vector2(-1.0, -3.0), Vector2(-2.0, -1.0), Vector2(-5.0, 1.0),
    Vector2(-2.0, -1.0)
]

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
    def saucer_surface(saucer_size):
        raw_points_span = Vector2(10, 6)
        raw_points_offset = raw_points_span / 2
        scale_factor = saucer_size.x / raw_points_span.x
        room_for_fat_line = Vector2(0, 2)
        saucer_surface = SurfaceMaker.create_scaled_surface(
            saucer_size + room_for_fat_line, raw_points_offset, scale_factor, raw_saucer_points)
        return saucer_surface

    @staticmethod
    def ship_surface(ship_size):
        raw_points_span = Vector2(14, 8)
        raw_points_offset = raw_points_span / 2
        scale_factor = ship_size.x / raw_points_span.x
        ship_surface = SurfaceMaker.create_scaled_surface(
            ship_size, raw_points_offset, scale_factor, raw_ship_points)
        return ship_surface

    @staticmethod
    def accelerating_surface(ship_size):
        raw_points_span = Vector2(14, 8)
        raw_points_offset = raw_points_span / 2
        scale_factor = ship_size.x / raw_points_span.x
        accelerating_surface = SurfaceMaker.create_scaled_surface(
            ship_size, raw_points_offset, scale_factor, raw_ship_points, raw_flare_points)
        return accelerating_surface

    @staticmethod
    def asteroid_surface(actual_size):
        raw_rock_points = SurfaceMaker.get_next_shape()
        raw_points_span = 8
        raw_points_offset = Vector2(4, 4)
        scale = actual_size / raw_points_span
        room_for_fat_line = 2
        surface_size = actual_size + room_for_fat_line
        surface = SurfaceMaker.create_scaled_surface((surface_size, surface_size),
                                                     raw_points_offset, scale, raw_rock_points)
        return surface

    @staticmethod
    def get_next_shape():
        rock_shape = raw_rocks[SurfaceMaker.next_shape]
        SurfaceMaker.next_shape = (SurfaceMaker.next_shape + 1) % 4
        return rock_shape

    @staticmethod
    def create_scaled_surface(dimensions, offset, scale_factor, *point_lists):
        surface = pygame.Surface(dimensions)
        surface.set_colorkey((0, 0, 0))
        # surface.fill("green")
        for point_list in point_lists:
            SurfaceMaker.draw_adjusted_lines(offset, point_list, scale_factor, surface)
        return surface

    @staticmethod
    def draw_adjusted_lines(offset, point_list, scale_factor, surface):
        adjusted = [SurfaceMaker.adjust(point, offset, scale_factor) for point in point_list]
        pygame.draw.lines(surface, "white", False, adjusted, 3)
