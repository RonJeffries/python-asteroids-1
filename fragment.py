import random

import pygame.draw
from pygame import Vector2

import u
from timer import Timer


class Fragment:

    @classmethod
    def simple_fragment(cls, position, angle=None, speed_mul=None):
        line = "line"
        half_length = random.uniform(6, 10)
        begin = Vector2(-half_length, 0)
        end = Vector2(half_length, 0)
        return cls(position, angle, speed_mul, [[line, begin, end]])

    @classmethod
    def v_fragment(cls, position, angle=None, speed_mul=None):
        line = "line"
        side_1 = [line, Vector2(-7, 5), Vector2(7, 0)]
        side_2 = [line, Vector2(7, 0), Vector2(-7, -5)]
        return cls(position, angle, speed_mul, [side_1, side_2])

    @classmethod
    def astronaut_fragment(cls, position, angle=None, speed_mul=None):
        line = "line"
        head = ["head", Vector2(0, 24), 8, 2]
        body_bottom = Vector2(0, 2)
        body = [line, Vector2(0, 16), body_bottom]
        left_leg = [line, Vector2(-5, -16), body_bottom]
        right_leg = [line, Vector2(5, -16), body_bottom]
        arm = [line, Vector2(-9, 10), Vector2(9, 10)]
        return cls(position, angle, speed_mul, [head, body, arm, left_leg, right_leg])

    def __init__(self, position, angle=None, speed_mul=None, fragments=None):
        angle = angle if angle is not None else random.randrange(360)
        self.position = position
        speed_mul = speed_mul if speed_mul is not None else random.uniform(0.25, 0.5)
        self.velocity = speed_mul*Vector2(u.FRAGMENT_SPEED, 0).rotate(angle)
        self.theta = random.randrange(0, 360)
        self.delta_theta = random.uniform(180, 360)*random.choice((1, -1))
        self.timer = Timer(u.FRAGMENT_LIFETIME, self.timeout)
        if not fragments:
            self.fragments = self.create_fragments()
        else:
            self.fragments = fragments

    def create_fragments(self):
        raise RuntimeError("should be unused")

    def draw(self, screen):
        self.draw_commands(screen, self.position, self.theta, self.fragments)

    def draw_commands(self, screen, position, theta, commands):
        for command in commands:
            operation = command[0]
            if operation == "line":
                self.draw_one_line(screen, position, theta, command[1:])
            elif operation == "head":
                self.draw_head(screen, command[1:])
            else:
                pass

    def draw_head(self, screen, parameters):
        position, radius, width = parameters
        head_off = position.rotate(self.theta)
        pygame.draw.circle(screen, "white", self.position + head_off, radius, width)

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

