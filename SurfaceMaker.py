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
