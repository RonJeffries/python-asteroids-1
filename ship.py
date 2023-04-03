# Ship

import pygame
from pygame import Vector2
import random
from SurfaceMaker import SurfaceMaker
import u
from mover import Mover


class Ship:
    def __init__(self, position):
        self.active = True
        self.radius = 25
        self.mover = Mover(position, Vector2(0,0))
        self.angle = 0
        self.acceleration = u.SHIP_ACCELERATION
        self.accelerating = False
        ship_scale = 4
        ship_size = Vector2(14, 8)*ship_scale
        self.ship_surface, self.ship_accelerating_surface = SurfaceMaker.ship_surfaces(ship_size)

    def collideWithAsteroid(self, asteroid):
        if asteroid.withinRange(self.mover.position, self.radius):
            self.active = False

    def draw(self, screen):
        ship_source = self.select_ship_source()
        rotated = pygame.transform.rotate(ship_source.copy(), self.angle)
        half = pygame.Vector2(rotated.get_size()) / 2
        screen.blit(rotated, self.mover.position - half)

    def power_on(self, dt):
        self.accelerating = True
        accel = dt * self.acceleration.rotate(-self.angle)
        self.mover.velocity += accel

    def power_off(self):
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
