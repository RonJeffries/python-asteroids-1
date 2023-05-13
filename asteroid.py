# Asteroid

from pygame.math import Vector2
import random

from SurfaceMaker import SurfaceMaker
import u
from movable_location import MovableLocation


class Flyer():
    def __init__(self):
        pass

    def destroyed_by(self, attacker, asteroids, fleets):
        pass


class Asteroid(Flyer):
    def __init__(self, size=2, position=None):
        super().__init__()
        self.size = size
        if self.size not in [0, 1, 2]:
            self.size = 2
        self.radius = [16, 32, 64][self.size]
        position = position if position is not None else Vector2(0, random.randrange(0, u.SCREEN_SIZE))
        angle_of_travel = random.randint(0, 360)
        velocity = u.ASTEROID_SPEED.rotate(angle_of_travel)
        self.location = MovableLocation(position, velocity)
        self.offset = Vector2(self.radius, self.radius)
        self.surface = SurfaceMaker.asteroid_surface(self.radius * 2)

    @property
    def position(self):
        return self.location.position

    @staticmethod
    def scores_for_hitting_asteroid():
        return [0, 0, 0]

    @staticmethod
    def scores_for_hitting_saucer():
        return [0, 0]

    def draw(self, screen):
        top_left_corner = self.position - self.offset
        screen.blit(self.surface, top_left_corner)

    def move(self, delta_time, _asteroids):
        self.location.move(delta_time)

    def move_to(self, vector):
        self.location.move_to(vector)

    def destroyed_by(self, attacker, asteroids, fleets):
        self.split_or_die(asteroids)

    def score_for_hitting(self, attacker):
        return attacker.scores_for_hitting_asteroid()[self.size]

    def split_or_die(self, asteroids):
        if self not in asteroids:
            return # already dead
        asteroids.remove(self)
        if self.size > 0:
            a1 = Asteroid(self.size - 1, self.position)
            asteroids.append(a1)
            a2 = Asteroid(self.size - 1, self.position)
            asteroids.append(a2)

    def tick(self, delta_time, fleet, _fleets):
        self.move(delta_time, fleet)
        return True
