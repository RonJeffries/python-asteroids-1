from itertools import repeat

import pygame

vector2 = pygame.Vector2

raw_rocks = [
    [
        vector2(4.0, 2.0), vector2(3.0, 0.0), vector2(4.0, -2.0),
        vector2(1.0, -4.0), vector2(-2.0, -4.0), vector2(-4.0, -2.0),
        vector2(-4.0, 2.0), vector2(-2.0, 4.0), vector2(0.0, 2.0),
        vector2(2.0, 4.0), vector2(4.0, 2.0),
    ],
    [
        vector2(2.0, 1.0), vector2(4.0, 2.0), vector2(2.0, 4.0),
        vector2(0.0, 3.0), vector2(-2.0, 4.0), vector2(-4.0, 2.0),
        vector2(-3.0, 0.0), vector2(-4.0, -2.0), vector2(-2.0, -4.0),
        vector2(-1.0, -3.0), vector2(2.0, -4.0), vector2(4.0, -1.0),
        vector2(2.0, 1.0)
    ],
    [
        vector2(-2.0, 0.0), vector2(-4.0, -1.0), vector2(-2.0, -4.0),
        vector2(0.0, -1.0), vector2(0.0, -4.0), vector2(2.0, -4.0),
        vector2(4.0, -1.0), vector2(4.0, 1.0), vector2(2.0, 4.0),
        vector2(-1.0, 4.0), vector2(-4.0, 1.0), vector2(-2.0, 0.0)
    ],
    [
        vector2(1.0, 0.0), vector2(4.0, 1.0), vector2(4.0, 2.0),
        vector2(1.0, 4.0), vector2(-2.0, 4.0), vector2(-1.0, 2.0),
        vector2(-4.0, 2.0), vector2(-4.0, -1.0), vector2(-2.0, -4.0),
        vector2(1.0, -3.0), vector2(2.0, -4.0), vector2(4.0, -2.0),
        vector2(1.0, 0.0)
    ]
]


def adjust(point, center_adjustment, scale_factor):
    return (point + center_adjustment) * scale_factor


def get_ship_points():
    ship_points = [vector2(-3.0, -2.0), vector2(-3.0, 2.0), vector2(-5.0, 4.0),
                   vector2(7.0, 0.0), vector2(-5.0, -4.0), vector2(-3.0, -2.0)]
    return list(map(adjust, ship_points, repeat(vector2(7, 4)), repeat(4)))


def get_flare_points():
    flare_points = [vector2(-3.0, -2.0), vector2(-7.0, 0.0), vector2(-3.0, 2.0)]
    return list(map(adjust, flare_points, repeat(vector2(7, 4)), repeat(4)))


def make_ship_surface(ship_points):
    ship_surface = pygame.Surface((60, 36))
    ship_surface.set_colorkey((0, 0, 0))
    pygame.draw.lines(ship_surface, "white", False, ship_points, 3)
    return ship_surface


def make_accelerating_surface(flare_points, ship_points):
    ship_accelerating_surface = make_ship_surface(ship_points)
    pygame.draw.lines(ship_accelerating_surface, "white", False, flare_points, 3)
    return ship_accelerating_surface


def prepare_surfaces():
    ship_points = get_ship_points()
    flare_points = get_flare_points()
    return (make_ship_surface(ship_points)), (make_accelerating_surface(flare_points, ship_points))


def prepare_surface():
    surface = pygame.Surface((128, 128))
    surface.set_colorkey((0, 0, 0))
    adjusted = list(map(adjust, raw_rocks[0], repeat(vector2(4,4)), repeat(16)))
    pygame.draw.lines(surface, "white", False, adjusted, 3)
    return surface
