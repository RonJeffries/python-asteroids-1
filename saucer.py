# Saucer

import random
from pygame import Vector2
import u
from SurfaceMaker import SurfaceMaker
from missile import Missile


class Saucer:
    def __init__(self, position=None, size=2):
        self.position = position if position is not None else u.CENTER
        self.size = size
        self.velocity = u.SAUCER_VELOCITY
        self.directions = (self.velocity.rotate(45), self.velocity, self.velocity, self.velocity.rotate(-45))
        self.direction = -1
        self.score_list = [0, 0, 0]
        self.radius = 20
        raw_dimensions = Vector2(10, 6)
        saucer_scale = 4*self.size
        self.offset = raw_dimensions*saucer_scale/2
        saucer_size = raw_dimensions*saucer_scale
        self.saucer_surface = SurfaceMaker.saucer_surface(saucer_size)
        self.zig_timer = 1.5
        self.missile_timer = u.SAUCER_MISSILE_DELAY

    def destroyed_by(self, attacker, saucers):
        if self in saucers: saucers.remove(self)

    def draw(self, screen):
        top_left_corner = self.position - self.offset
        screen.blit(self.saucer_surface, top_left_corner)

    def init_for_new_game(self):
        self.direction = -1

    def move(self, delta_time, saucers):
        self.check_zigzag(delta_time)
        self.position += delta_time*self.velocity
        x = self.position.x
        if x < 0 or x > u.SCREEN_SIZE:
            if self in saucers:
                saucers.remove(self)

    def check_zigzag(self, delta_time):
        self.zig_timer -= delta_time
        if self.zig_timer <= 0:
            self.zig_timer = u.SAUCER_ZIG_TIME
            self.velocity = self.new_direction()*self.direction

    def new_direction(self):
        return random.choice(self.directions)

    def fire_if_possible(self, delta_time, saucer_missiles):
        self.missile_timer -= delta_time
        if self.missile_timer <= 0 and len(saucer_missiles) < u.SAUCER_MISSILE_LIMIT:
            saucer_missiles.append(self.create_missile())
            self.missile_timer = u.SAUCER_MISSILE_DELAY

    def create_missile(self):
        return Missile(u.CENTER, Vector2(70, 70))

    def ready(self):
        self.direction = -self.direction
        self.velocity = self.direction*u.SAUCER_VELOCITY
        x = 0 if self.direction > 0 else u.SCREEN_SIZE
        self.position = Vector2(x, random.randrange(0, u.SCREEN_SIZE))
        self.missile_timer = u.SAUCER_MISSILE_DELAY
        self.zig_timer = u.SAUCER_ZIG_TIME

    def score_against(self, _):
        return 0