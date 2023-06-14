# Ship

import pygame
from pygame import Vector2
import random
from SurfaceMaker import SurfaceMaker
import u
from explosion import Explosion
from flyer import Flyer
from hyperspace_generator import HyperspaceGenerator
from missile import Missile
from movable_location import MovableLocation
from sounds import player
from timer import Timer


class Ship(Flyer):
    thrust_sound = None

    def __init__(self, position):
        self.radius = 25
        self._location = MovableLocation(position, Vector2(0, 0))
        self._hyperspace_generator = HyperspaceGenerator(self)
        self._hyperspace_timer = Timer(u.SHIP_HYPERSPACE_RECHARGE_TIME)
        self._can_fire = True
        self._angle = 0
        self._acceleration = u.SHIP_ACCELERATION
        self._accelerating = False
        self._asteroid_tally = 0
        self._missile_tally = 0
        ship_scale = 4
        ship_size = Vector2(14, 8)*ship_scale
        self._ship_surface, self._ship_accelerating_surface = SurfaceMaker.ship_surfaces(ship_size)

    @property
    def position(self):
        return self._location.position

    @property
    def velocity_testing_only(self):
        return self._location.velocity

    @velocity_testing_only.setter
    def velocity_testing_only(self, velocity):
        self._location.velocity = velocity

    @staticmethod
    def scores_for_hitting_asteroid():
        return [0, 0, 0]

    @staticmethod
    def scores_for_hitting_saucer():
        return [0, 0]

    def accelerate_by(self, accel):
        self._location.accelerate_by(accel)

    def accelerate_to(self, accel):
        self._location.accelerate_to(accel)

    def control_motion(self, delta_time, fleets):
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
        if keys[pygame.K_SPACE]:
            self._hyperspace_generator.press_button(self._asteroid_tally, fleets)
        else:
            self._hyperspace_generator.lift_button()

    def control_firing(self, fleets):
        if not pygame.get_init():
            return
        if pygame.key.get_pressed()[pygame.K_k]:
            self.fire_if_possible(fleets)
        else:
            self._can_fire = True

    def interact_with(self, attacker, fleets):
        attacker.interact_with_ship(self, fleets)

    def begin_interactions(self, fleets):
        self._asteroid_tally = 0
        self._missile_tally = 0

    def interact_with_asteroid(self, asteroid, fleets):
        self._asteroid_tally += 1
        self.explode_if_hit(fleets, asteroid)

    def interact_with_missile(self, missile, fleets):
        self._missile_tally += 1
        self.explode_if_hit(fleets, missile)

    def interact_with_saucermissile(self, missile, fleets):
        self.explode_if_hit(fleets, missile)

    def explode_if_hit(self, fleets, attacker):
        if attacker.are_we_colliding(self.position, self.radius):
            self.explode(fleets)

    def interact_with_saucer(self, saucer, fleets):
        self.explode_if_hit(fleets, saucer)

    def are_we_colliding(self, position, radius):
        kill_range = self.radius + radius
        dist = self.position.distance_to(position)
        return dist <= kill_range

    @staticmethod
    def score_for_hitting(_anyone):
        return 0

    def draw(self, screen):
        ship_source = self.select_ship_source()
        rotated = pygame.transform.rotate(ship_source.copy(), self._angle)
        half = pygame.Vector2(rotated.get_size()) / 2
        screen.blit(rotated, self.position - half)

    def explode(self, fleets):
        player.play("bang_large", self._location)
        fleets.remove_flyer(self)
        fleets.add_flyer(Explosion.from_ship(self.position))

    def fire_if_possible(self, fleets):
        if self._can_fire and self._missile_tally < u.MISSILE_LIMIT:
            fleets.add_flyer(self.create_missile())
            self._can_fire = False

    def create_missile(self):
        player.play("fire", self._location)
        return Missile.from_ship(self.missile_start(), self.missile_velocity())

    def missile_start(self):
        start_distance = self.radius + Missile.radius + 1
        offset = Vector2(start_distance, 0).rotate(-self._angle)
        return self.position + offset

    def missile_velocity(self):
        return Vector2(u.MISSILE_SPEED, 0).rotate(-self._angle) + self.velocity_testing_only

    def move_to(self, vector):
        self._location.move_to(vector)

    def power_on(self, dt):
        self._accelerating = True
        player.play("accelerate", self._location, False)
        accel = dt * self._acceleration.rotate(-self._angle)
        self.accelerate_by(accel)

    def power_off(self):
        self._accelerating = False

    def reset(self):
        self.move_to(u.CENTER)
        self.accelerate_to(Vector2(0, 0))
        self._angle = 0

    def select_ship_source(self):
        if self._accelerating and random.random() >= 0.66:
            return self._ship_accelerating_surface
        else:
            return self._ship_surface

    def tick(self, delta_time, fleets):
        self._hyperspace_generator.tick(delta_time)

    def update(self, delta_time, fleets):
        self.control_motion(delta_time, fleets)
        self._location.move(delta_time)
        self.control_firing(fleets)

    def turn_left(self, dt):
        self._angle = self._angle - u.SHIP_ROTATION_STEP * dt

    def turn_right(self, dt):
        self._angle = self._angle + u.SHIP_ROTATION_STEP * dt
