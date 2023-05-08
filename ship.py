# Ship

import pygame
from pygame import Vector2
import random
from SurfaceMaker import SurfaceMaker
import u
from missile import Missile


class Ship:
    def __init__(self, position):
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

    def scores_for_hitting_asteroid(self):
        return [0, 0, 0]

    def scores_for_hitting_saucer(self):
        return [0, 0]

    def accelerate_by(self, accel):
        self.velocity = self.velocity + accel

    def control_motion(self, delta_time, missiles):
        if not pygame.get_init():
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            self.turn_left(delta_time)
        if keys[pygame.K_d]:
            self.turn_right(delta_time)
        if keys[pygame.K_j]:
            self.power_on(delta_time)
        else:
            self.power_off()
        if keys[pygame.K_k]:
            self.fire_if_possible(missiles)
        else:
            self.can_fire = True

    def destroyed_by(self, attacker, ships):
        if self in ships: ships.remove(self)

    def score_for_hitting(self, _anyone):
        return 0

    def within_range(self, point, other_radius):
        dist = point.distance_to(self.position)
        return dist < self.radius + other_radius

    def draw(self, screen):
        ship_source = self.select_ship_source()
        rotated = pygame.transform.rotate(ship_source.copy(), self.angle)
        half = pygame.Vector2(rotated.get_size()) / 2
        screen.blit(rotated, self.position - half)

    def fire_if_possible(self, missiles):
        if self.can_fire and missiles.fire(self.create_missile):
            self.can_fire = False

    def create_missile(self):
        return Missile.from_ship(self.missile_start(), self.missile_velocity())

    def missile_start(self):
        radius = self.radius + 11
        offset = Vector2(radius, 0).rotate(-self.angle)
        return self.position + offset

    def missile_velocity(self):
        return Vector2(u.MISSILE_SPEED, 0).rotate(-self.angle) + self.velocity

    def move(self, delta_time, _ships):
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

    def tick(self, delta_time, fleet, fleets):
        self.control_motion(delta_time, fleets.missiles)
        self.move(delta_time, fleet)
        return True

    def turn_left(self, dt):
        self.angle = self.angle - u.SHIP_ROTATION_STEP * dt

    def turn_right(self, dt):
        self.angle = self.angle + u.SHIP_ROTATION_STEP * dt
