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
        pygame.draw.line(screen, "red", begin, end, 3)

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
