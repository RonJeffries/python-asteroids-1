import random

import pygame.draw
from pygame import Vector2

import u
from flyer import Flyer
from timer import Timer


class LineCommand:
    def __init__(self, pos1, pos2):
        self._pos1 = pos1
        self._pos2 = pos2

    def draw(self, screen, position, theta):
        p1 = position + self._pos1.rotate(theta)
        p2 = position + self._pos2.rotate(theta)
        pygame.draw.line(screen, "white", p1, p2, 3)


class CircleCommand:
    def __init__(self, position, radius, width):
        self._pos = position
        self._radius = radius
        self._width = width

    def draw(self, screen, position, theta):
        head_off = self._pos.rotate(theta)
        pygame.draw.circle(screen, "white", position + head_off, self._radius, self._width)


class Fragment(Flyer):
    @classmethod
    def simple_fragment(cls, position, angle=None, speed_mul=None):
        half_length = random.uniform(6, 10)
        begin = Vector2(-half_length, 0)
        end = Vector2(half_length, 0)
        frag = LineCommand(begin, end)
        return cls(position, angle, speed_mul, [frag])

    @classmethod
    def v_fragment(cls, position, angle=None, speed_mul=None):
        side_1 = LineCommand(Vector2(-7, 5), Vector2(7, 0))
        side_2 = LineCommand(Vector2(7, 0), Vector2(-7, -5))
        return cls(position, angle, speed_mul, [side_1, side_2])

    @classmethod
    def astronaut_fragment(cls, position, angle=None, speed_mul=None):
        head = CircleCommand(Vector2(0, 24), 8, 2)
        body_bottom = Vector2(0, 2)
        body = LineCommand(Vector2(0, 16), body_bottom)
        left_leg = LineCommand(Vector2(-5, -16), body_bottom)
        right_leg = LineCommand(Vector2(5, -16), body_bottom)
        arm = LineCommand(Vector2(-9, 10), Vector2(9, 10))
        return cls(position, angle, speed_mul, [head, body, arm, left_leg, right_leg])

    def __init__(self, position, angle=None, speed_mul=None, fragments=None):
        angle = angle if angle is not None else random.randrange(360)
        self.position = position
        speed_mul = speed_mul if speed_mul is not None else random.uniform(0.25, 0.5)
        self.velocity = speed_mul*Vector2(u.FRAGMENT_SPEED, 0).rotate(angle)
        self.theta = random.randrange(0, 360)
        self.delta_theta = random.uniform(180, 360)*random.choice((1, -1))
        self.timer = Timer(u.FRAGMENT_LIFETIME)
        self.fragments = fragments

    @staticmethod
    def are_we_colliding(_position, _radius):
        return False

    def draw(self, screen):
        for command in self.fragments:
            command.draw(screen, self.position, self.theta)

    def interact_with(self, attacker, fleets):
        attacker.interact_with_fragment(self, fleets)

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass

    def update(self, delta_time, _fleets):
        position = self.position + self.velocity * delta_time
        position.x = position.x % u.SCREEN_SIZE
        position.y = position.y % u.SCREEN_SIZE
        self.position = position
        self.theta += self.delta_theta*delta_time

    def tick(self, delta_time, fleets):
        self.timer.tick(delta_time, self.timeout, fleets)

    def timeout(self, fleets):
        fleets.remove(self)

