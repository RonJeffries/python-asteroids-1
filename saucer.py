# Saucer
import pygame
from pygame import Vector2

from SurfaceMaker import SurfaceMaker


class Saucer:
    def __init__(self, position=None):
        if position is not None: self.position = position
        self.score_list = [0, 0, 0]
        self.radius = 20
        base_size = Vector2(10, 6)
        saucer_scale = 4
        self.offset = base_size*saucer_scale/2
        saucer_size = base_size*saucer_scale
        self.saucer_surface = SurfaceMaker.saucer_surface(saucer_size)

    def destroyed_by(self, attacker, saucers):
        if self in saucers: saucers.remove(self)

    def draw(self, screen):
        top_left_corner = self.position - self.offset
        screen.blit(self.saucer_surface, top_left_corner)

    def score_against(self, _):
        return 0