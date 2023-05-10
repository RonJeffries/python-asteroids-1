import random

import pygame.draw
from pygame import Vector2

import u
from timer import Timer


class Fragment:
    def __init__(self, position, angle=None, speed_mul=None):
        angle = angle if angle is not None else random.randrange(360)
        self.position = position
        speed_mul = speed_mul if speed_mul is not None else random.uniform(0.25, 0.5)
        self.velocity = speed_mul*Vector2(u.FRAGMENT_SPEED, 0).rotate(angle)
        self.theta = random.randrange(0, 360)
        self.delta_theta = random.uniform(180, 360)*random.choice((1, -1))
        self.timer = Timer(u.FRAGMENT_LIFETIME, self.timeout)
        half_length = random.uniform(6, 10)
        begin = Vector2(-half_length, 0)
        end = Vector2(half_length, 0)
        self.frags = [[begin, end]]

    def draw(self, screen):
        self.draw_lines(screen, self.position, self.theta, self.frags)

    def draw_lines(self, screen, position, theta, pairs):
        for pair in pairs:
            self.draw_one_line(screen, position, theta, pair)

    def draw_one_line(self, screen, position, theta, pair):
        start = pair[0].rotate(theta) + position
        end = pair[1].rotate(theta) + position
        pygame.draw.line(screen, "white", start, end, 3)

    def move(self, delta_time):
        position = self.position + self.velocity * delta_time
        position.x = position.x % u.SCREEN_SIZE
        position.y = position.y % u.SCREEN_SIZE
        self.position = position
        self.theta += self.delta_theta*delta_time

    def tick(self, delta_time, fragments, _fleets):
        self.timer.tick(delta_time, fragments)
        self.move(delta_time)

    def timeout(self, fragments):
        fragments.remove(self)


class VFragment(Fragment):
    def __init__(self, position, angle=None, speed_mul=None):
        super().__init__(position, angle, speed_mul)

    def draw(self, screen):
        side_1 = [Vector2(-7, 5), Vector2(7, 0)]
        side_2 = [Vector2(7, 0), Vector2(-7, -5)]
        v = [side_1, side_2]
        self.draw_lines(screen, self.position, self.theta, v)


class GFragment(Fragment):
    def __init__(self, position, angle=None, speed_mul=None):
        super().__init__(position, angle, speed_mul)

    def draw(self, screen):
        head_off = Vector2(0, 16 + 8).rotate(self.theta)
        pygame.draw.circle(screen, "white", self.position + head_off, 8, 2)
        body_bottom = Vector2(0, 2)
        body = [Vector2(0, 16), body_bottom]
        left_leg = [Vector2(-5, -16), body_bottom]
        right_leg = [Vector2(5, -16), body_bottom]
        arm = [Vector2(-9, 10), Vector2(9, 10)]
        pairs = [body, arm, left_leg, right_leg]
        self.draw_lines(screen, self.position, self.theta, pairs)
