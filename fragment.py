import random

import pygame.draw
from pygame import Vector2

import u
from timer import Timer


class Fragment:
    def __init__(self, position, angle=None, speed_mul=None):
        angle = angle if angle is not None else random.randrange(360)
        self.position = position
        half_length = random.uniform(6, 10)
        self.begin = Vector2(-half_length, 0)
        self.end = Vector2(half_length, 0)
        speed_mul = speed_mul if speed_mul is not None else random.uniform(0.25, 0.5)
        self.velocity = speed_mul*Vector2(u.FRAGMENT_SPEED, 0).rotate(angle)
        self.theta = random.randrange(0, 360)
        self.delta_theta = random.uniform(180, 360)*random.choice((1, -1))
        self.timer = Timer(u.FRAGMENT_LIFETIME, self.timeout)

    def draw(self, screen):
        begin = self.position + self.begin.rotate(self.theta)
        end = self.position + self.end.rotate(self.theta)
        pygame.draw.line(screen, "white", begin, end, 3)

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
        v_shape = [Vector2(-7, 5), Vector2(7, 0), Vector2(-7, -5)]
        points = [p.rotate(self.theta) + self.position for p in v_shape]
        pygame.draw.lines(screen, "white", False, points, 3)

class GFragment(Fragment):
    def __init__(self, position, angle=None, speed_mul=None):
        super().__init__(position, angle, speed_mul)

    def draw(self, screen):
        theta = self.theta
        head_off = Vector2(0,16+8).rotate(theta)
        position = self.position
        pygame.draw.circle(screen, "white", position + head_off, 8, 2)
        body_top = Vector2(0, 16).rotate(theta)
        body_bottom = Vector2(0, 2).rotate(theta)
        pygame.draw.line(screen, "white", body_top + position, body_bottom + position, 3)
        leg_left = Vector2(-5, -16).rotate(theta)
        pygame.draw.line(screen, "white", leg_left + position, body_bottom + position, 3)
        leg_right = Vector2(5, -16).rotate(theta)
        pygame.draw.line(screen, "white", leg_right + position, body_bottom + position, 3)
        pair = [(Vector2(-9, 10)), (Vector2(9, 10))]
        self.draw_one_line(pair, position, screen, theta)

    def draw_one_line(self, pair, position, screen, theta):
        start = pair[0].rotate(theta) + position
        end = pair[1].rotate(theta) + position
        pygame.draw.line(screen, "white", start, end, 3)
