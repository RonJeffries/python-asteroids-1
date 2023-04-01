import pygame
import random

from pygame import Vector2

import u
from SurfaceMaker import SurfaceMaker

vector2 = pygame.Vector2


class Ship:
    def __init__(self, position):
        self.position = position
        self.velocity = vector2(0, 0)
        self.angle = 0
        self.acceleration = u.SHIP_ACCELERATION
        self.accelerating = False
        ship_scale = 4
        ship_size = Vector2(14, 8)*4
        self.ship_surface, self.ship_accelerating_surface = SurfaceMaker.ship_surfaces(ship_size)

    def draw(self, screen):
        ship_source = self.select_ship_source()
        rotated = pygame.transform.rotate(ship_source.copy(), self.angle)
        half = pygame.Vector2(rotated.get_size()) / 2
        screen.blit(rotated, self.position - half)

    def move(self, dt):
        self.position += self.velocity * dt
        self.position.x = self.position.x % u.SCREEN_SIZE
        self.position.y = self.position.y % u.SCREEN_SIZE

    def power_on(self, dt):
        self.accelerating = True
        accel = dt * self.acceleration.rotate(-self.angle)
        self.velocity += accel

    def power_off(self, dt):
        self.accelerating = False

    def select_ship_source(self):
        if self.accelerating and random.random() >= 0.66:
            return self.ship_accelerating_surface
        else:
            return self.ship_surface

    def turn_left(self, dt):
        self.angle -= u.SHIP_ROTATION_STEP * dt

    def turn_right(self, dt):
        self.angle += u.SHIP_ROTATION_STEP * dt
