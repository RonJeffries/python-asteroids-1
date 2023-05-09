import random

import pygame.draw
from pygame import Vector2

import u
from timer import Timer


class Fragment():
    def __init__(self, position, angle=None):
        angle = angle if angle is not None else random.randrange(360)
        self.position = position
        self.velocity = Vector2(u.FRAGMENT_SPEED, 0).rotate(angle)
        self.timer = Timer(u.FRAGMENT_LIFETIME, self.timeout)

    def draw(self, screen):
        begin = self.position + Vector2(-3,0)
        end = self.position + Vector2(3,0)
        pygame.draw.line(screen, "red", begin, end, 3)

    def move(self, delta_time):
        position = self.position + self.velocity * delta_time
        position.x = position.x % u.SCREEN_SIZE
        position.y = position.y % u.SCREEN_SIZE
        self.position = position

    def tick(self, delta_time, fragments, _fleets):
        self.timer.tick(delta_time, fragments)
        self.move(delta_time)

    def timeout(self, fragments):
        fragments.remove(self)
