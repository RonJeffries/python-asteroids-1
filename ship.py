from itertools import repeat

import pygame
import random
import u
from SurfaceMaker import adjust

vector2 = pygame.Vector2


class Ship:
    def __init__(self, position):
        self.position = position
        self.velocity = vector2(0, 0)
        self.angle = 0
        self.acceleration = u.SHIP_ACCELERATION
        self.accelerating = False
        self.ship_surface, self.ship_accelerating_surface = self.prepare_surfaces()

    def prepare_surfaces(self):
        ship_points = self.get_ship_points()
        flare_points = self.get_flare_points()
        return (self.make_ship_surface(ship_points)), (self.make_accelerating_surface(flare_points, ship_points))

    def make_accelerating_surface(self, flare_points, ship_points):
        ship_accelerating_surface = self.make_ship_surface(ship_points)
        pygame.draw.lines(ship_accelerating_surface, "white", False, flare_points, 3)
        return ship_accelerating_surface

    def make_ship_surface(self, ship_points):
        ship_surface = pygame.Surface((60, 36))
        ship_surface.set_colorkey((0, 0, 0))
        pygame.draw.lines(ship_surface, "white", False, ship_points, 3)
        return ship_surface

    def get_flare_points(self):
        flare_points = [vector2(-3.0, -2.0), vector2(-7.0, 0.0), vector2(-3.0, 2.0)]
        return list(map(adjust, flare_points, repeat(vector2(7, 4)), repeat(4)))

    def get_ship_points(self):
        ship_points = [vector2(-3.0, -2.0), vector2(-3.0, 2.0), vector2(-5.0, 4.0),
                       vector2(7.0, 0.0), vector2(-5.0, -4.0), vector2(-3.0, -2.0)]
        return list(map(adjust, ship_points, repeat(vector2(7, 4)), repeat(4)))

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
