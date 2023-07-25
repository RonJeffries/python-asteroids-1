# SurfaceMaker
import random

import pygame
from pygame import Vector2

import u

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


class Painter:
    def __init__(self, points, scale):
        self._points = points
        self._scale = scale

    def draw(self, screen, position, angle=0, scale_adjustment=1):
        draw_lines(screen, self._points, position, self._scale*scale_adjustment, angle)

    @classmethod
    def saucer(cls, scale):
        return cls(raw_saucer_points, scale)

    @classmethod
    def asteroid(cls, radius):
        which_one = random.randint(0, 3)
        scale = radius / 4
        return cls(raw_rocks[which_one], scale)

    @classmethod
    def ship(cls):
        scale = 4 * u.SCALE_FACTOR
        return cls(raw_ship_points, scale)

    @classmethod
    def ship_accelerating(cls):
        scale = 4 * u.SCALE_FACTOR
        return cls(raw_ship_points + raw_flare_points, scale)



def draw_lines(screen, points, position, scale, angle=0):
    adjusted = [(point.rotate(-angle) * scale) + position for point in points]
    pygame.draw.lines(screen, "white", False, adjusted, 3)