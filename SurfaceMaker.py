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
    def accelerating_surface(object_size: Vector2):
        points_to_draw = raw_flare_points
        room_for_fat_line = Vector2(0, 0)
        raw_points_span = Vector2(14, 8)
        return SurfaceMaker.create_desired_surface(points_to_draw, object_size, raw_points_span, room_for_fat_line)

    @staticmethod
    def create_desired_surface(points_to_draw, object_size, raw_points_span, room_for_fat_line):
        raw_points_offset = raw_points_span / 2
        scale_factor = object_size.x / raw_points_span.x
        expanded_size = object_size + room_for_fat_line
        surface = SurfaceMaker.create_scaled_surface(
            expanded_size, raw_points_offset, scale_factor, points_to_draw)
        return surface

    @staticmethod
    def asteroid_surface(object_size: Vector2):
        points_to_draw = SurfaceMaker.get_next_shape()
        room_for_fat_line = Vector2(2, 2)
        raw_points_span = Vector2(8, 8)
        return SurfaceMaker.create_desired_surface(points_to_draw, object_size, raw_points_span, room_for_fat_line)

    @staticmethod
    def saucer_surface(object_size: Vector2):
        points_to_draw = raw_saucer_points
        room_for_fat_line = Vector2(0, 2)
        raw_points_span = Vector2(10, 6)
        return SurfaceMaker.create_desired_surface(points_to_draw, object_size, raw_points_span, room_for_fat_line)

    @staticmethod
    def ship_surface(object_size: Vector2):
        points_to_draw = raw_ship_points
        room_for_fat_line = Vector2(0, 0)
        raw_points_span = Vector2(14, 8)
        return SurfaceMaker.create_desired_surface(points_to_draw, object_size, raw_points_span, room_for_fat_line)

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
