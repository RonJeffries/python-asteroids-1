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

    def move(self, delta_time, saucers, saucer_missiles):
        self.fire_if_possible(delta_time, saucer_missiles)
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
        if self.firing_is_possible(delta_time, saucer_missiles):
            self.fire_a_missile(saucer_missiles)

    def fire_a_missile(self, saucer_missiles):
        saucer_missiles.append(self.create_missile())
        self.missile_timer = u.SAUCER_MISSILE_DELAY

    def firing_is_possible(self, delta_time, saucer_missiles):
        return self.missile_timer_expired(delta_time) and self.a_missile_is_available(saucer_missiles)

    def missile_at_angle(self, degrees):
        missile_velocity = Vector2(u.MISSILE_SPEED, 0).rotate(degrees)
        offset = Vector2(2*self.radius, 0).rotate(degrees)
        return Missile(self.position + offset, self.velocity + missile_velocity)

    def missile_timer_expired(self, delta_time):
        self.missile_timer -= delta_time
        expired = self.missile_timer <= 0
        return expired

    @staticmethod
    def a_missile_is_available(saucer_missiles):
        return len(saucer_missiles) < u.SAUCER_MISSILE_LIMIT

    def create_missile(self):
        degrees = random.random()*360.0
        return self.missile_at_angle(degrees)

    def ready(self):
        self.direction = -self.direction
        self.velocity = self.direction*u.SAUCER_VELOCITY
        x = 0 if self.direction > 0 else u.SCREEN_SIZE
        self.position = Vector2(x, random.randrange(0, u.SCREEN_SIZE))
        self.missile_timer = u.SAUCER_MISSILE_DELAY
        self.zig_timer = u.SAUCER_ZIG_TIME

    def score_against(self, _):
        return 0