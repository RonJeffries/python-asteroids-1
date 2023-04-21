# Saucer

import random
from pygame import Vector2
import u
from SurfaceMaker import SurfaceMaker


class Saucer:
    def __init__(self, position=None, size=2):
        self.position = position if position is not None else u.CENTER
        self.size = size
        self.velocity = u.SAUCER_VELOCITY
        self.direction = 1
        self.score_list = [0, 0, 0]
        self.radius = 20
        raw_dimensions = Vector2(10, 6)
        saucer_scale = 4*self.size
        self.offset = raw_dimensions*saucer_scale/2
        saucer_size = raw_dimensions*saucer_scale
        self.saucer_surface = SurfaceMaker.saucer_surface(saucer_size)

    def destroyed_by(self, attacker, saucers):
        if self in saucers: saucers.remove(self)

    def draw(self, screen):
        top_left_corner = self.position - self.offset
        screen.blit(self.saucer_surface, top_left_corner)

    def init_for_new_game(self):
        self.direction = 1

    def move(self, delta_time, saucers):
        self.position += delta_time*self.velocity
        x = self.position.x
        if x < 0 or x > u.SCREEN_SIZE:
            if self in saucers:
                saucers.remove(self)

    def ready(self):
        self.velocity = self.direction*u.SAUCER_VELOCITY
        x = 0 if self.direction > 0 else u.SCREEN_SIZE
        self.position = Vector2(x, random.randrange(0, u.SCREEN_SIZE))
        self.direction = -self.direction

    def score_against(self, _):
        return 0