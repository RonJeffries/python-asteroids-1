# Asteroid

from pygame.math import Vector2
import random

from SurfaceMaker import SurfaceMaker
import u

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
        self.position = position if position is not None else Vector2(0, random.randrange(0, u.SCREEN_SIZE))
        angle_of_travel = random.randint(0, 360)
        self.velocity = u.ASTEROID_SPEED.rotate(angle_of_travel)
        self.offset = Vector2(self.radius, self.radius)
        self.surface = SurfaceMaker.asteroid_surface(self.radius * 2)

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
        position = self.position + self.velocity * delta_time
        position.x = position.x % u.SCREEN_SIZE
        position.y = position.y % u.SCREEN_SIZE
        self.position = position

    def within_range(self, point, other_radius):
        dist = point.distance_to(self.position)
        return dist < self.radius + other_radius

    def destroyed_by(self, attacker, asteroids, fleets):
        self.split_or_die(asteroids)

    def score_for_hitting(self, attacker):
        return attacker.scores_for_hitting_asteroid()[self.size]

    def split_or_die(self, asteroids):
        if self not in asteroids: return # already dead
        asteroids.remove(self)
        if self.size > 0:
            a1 = Asteroid(self.size - 1, self.position)
            asteroids.append(a1)
            a2 = Asteroid(self.size - 1, self.position)
            asteroids.append(a2)

    def tick(self, delta_time, fleet, _fleets):
        self.move(delta_time, fleet)
        return True
