# Ship

import pygame
from pygame import Vector2
import random
from SurfaceMaker import SurfaceMaker
import u
from missile import Missile


class Ship:
    def __init__(self, position):
        self.score_list = [0, 0, 0]
        self.position = position.copy()
        self.velocity = Vector2(0, 0)
        self.can_fire = True
        self.radius = 25
        self.angle = 0
        self.acceleration = u.SHIP_ACCELERATION
        self.accelerating = False
        ship_scale = 4
        ship_size = Vector2(14, 8)*ship_scale
        self.ship_surface, self.ship_accelerating_surface = SurfaceMaker.ship_surfaces(ship_size)

    def accelerate_by(self, accel):
        self.velocity = self.velocity + accel

    def collide_with_attacker(self, attacker, attackers, ships):
        if self.within_range(attacker.position, attacker.radius):
            attacker.destroyed_by(self, attackers)
            self.destroyed_by(attacker, ships)

    def destroyed_by(self, attacker, ships):
        if self in ships: ships.remove(self)

    def within_range(self, point, other_radius):
        dist = point.distance_to(self.position)
        return dist < self.radius + other_radius

    def draw(self, screen):
        ship_source = self.select_ship_source()
        rotated = pygame.transform.rotate(ship_source.copy(), self.angle)
        half = pygame.Vector2(rotated.get_size()) / 2
        screen.blit(rotated, self.position - half)

    def fire_if_possible(self, missiles):
        if self.can_fire and len(missiles) < u.MISSILE_LIMIT:
            missiles.append(Missile(self.missile_start(), self.missile_velocity()))
            self.can_fire = False

    def not_firing(self):
        self.can_fire = True

    def missile_start(self):
        radius = self.radius + 11
        offset = Vector2(radius, 0).rotate(-self.angle)
        return self.position + offset

    def missile_velocity(self):
        return Vector2(u.MISSILE_SPEED, 0).rotate(-self.angle) + self.velocity

    def move(self, delta_time):
        position = self.position + self.velocity * delta_time
        position.x = position.x % u.SCREEN_SIZE
        position.y = position.y % u.SCREEN_SIZE
        self.position = position

    def power_on(self, dt):
        self.accelerating = True
        accel = dt * self.acceleration.rotate(-self.angle)
        self.accelerate_by(accel)

    def power_off(self):
        self.accelerating = False

    def reset(self):
        self.position = u.CENTER
        self.velocity = Vector2(0, 0)
        self.angle = 0

    def select_ship_source(self):
        if self.accelerating and random.random() >= 0.66:
            return self.ship_accelerating_surface
        else:
            return self.ship_surface

    def turn_left(self, dt):
        self.angle = self.angle - u.SHIP_ROTATION_STEP * dt

    def turn_right(self, dt):
        self.angle = self.angle + u.SHIP_ROTATION_STEP * dt
