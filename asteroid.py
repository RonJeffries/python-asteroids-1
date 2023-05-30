# Asteroid

from pygame.math import Vector2
import random

from SurfaceMaker import SurfaceMaker
import u
from flyer import Flyer
from movable_location import MovableLocation
from score import Score
from sounds import player


class Asteroid(Flyer):
    def __init__(self, size=2, position=None):
        self.size = size
        if self.size not in [0, 1, 2]:
            self.size = 2
        self.radius = [16, 32, 64][self.size]
        position = position if position is not None else Vector2(0, random.randrange(0, u.SCREEN_SIZE))
        angle_of_travel = random.randint(0, 360)
        velocity = u.ASTEROID_SPEED.rotate(angle_of_travel)
        self._location = MovableLocation(position, velocity)
        self._offset = Vector2(self.radius, self.radius)
        self._surface = SurfaceMaker.asteroid_surface(self.radius * 2)

    @property
    def position(self):
        return self._location.position

    @staticmethod
    def scores_for_hitting_asteroid():
        return [0, 0, 0]

    @staticmethod
    def scores_for_hitting_saucer():
        return [0, 0]

    def draw(self, screen):
        top_left_corner = self.position - self._offset
        screen.blit(self._surface, top_left_corner)

    def move(self, delta_time, _asteroids):
        self._location.move(delta_time)

    def move_to(self, vector):
        self._location.move_to(vector)

    def interact_with(self, attacker, fleets):
        attacker.interact_with_asteroid(self, fleets)

    def interact_with_missile(self, missile, fleets):
        if missile.are_we_colliding(self.position, self.radius):
            fleets.add_flyer(Score(self.score_for_hitting(missile)))
            self.split_or_die(fleets)

    def interact_with_saucer(self, saucer, fleets):
        if saucer.are_we_colliding(self.position, self.radius):
            self.split_or_die(fleets)

    def interact_with_ship(self, ship, fleets):
        if ship.are_we_colliding(self.position, self.radius):
            self.split_or_die(fleets)

    def are_we_colliding(self, position, radius):
        kill_range = self.radius + radius
        dist = self.position.distance_to(position)
        return dist <= kill_range

    def score_for_hitting(self, attacker):
        return attacker.scores_for_hitting_asteroid()[self.size]

    def split_or_die(self, fleets):
        fleets.remove_flyer(self)
        self.explode()
        if self.size > 0:
            a1 = Asteroid(self.size - 1, self.position)
            fleets.add_flyer(a1)
            a2 = Asteroid(self.size - 1, self.position)
            fleets.add_flyer(a2)

    def explode(self):
        sound = ["bang_small", "bang_medium", "bang_large"][self.size]
        player.play(sound, self._location)

    def tick(self, delta_time, fleet, _fleets):
        self.move(delta_time, fleet)
