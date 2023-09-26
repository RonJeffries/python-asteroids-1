# SurfaceMaker

from pygame import Vector2
import random
import pygame
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
        scale = self._scale * scale_adjustment
        adjusted = [(point.rotate(-angle) * scale) + position for point in self._points]
        pygame.draw.lines(screen, "white", False, adjusted, 3)

    @classmethod
    def saucer(cls, scale):
        # scale = 4 or 8 * u.SCALE_FACTOR
        # note ship is 4 * u.SCALE_FACTOR
        return cls(raw_saucer_points, scale)

    @classmethod
    def asteroid(cls, radius):
        # radius = 16, 32, or 64 * u.SCALE_FACTOR
        # scale = 4, 8, or 16 * u.SCALE_FACTOR
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



