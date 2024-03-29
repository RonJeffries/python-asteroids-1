import random

from pygame import Vector2
import u
from asteroids.aimimprover import AimImprover
from asteroids.missile import Missile


class FiringSolution:
    def __init__(self, target_position, shooter_position, safe_distance):
        direction_to_target = (target_position - shooter_position).normalize()
        safety_offset = direction_to_target * safe_distance
        self.velocity = direction_to_target * u.MISSILE_SPEED
        self.start = shooter_position + safety_offset

    def saucer_missile(self):
        return Missile("saucer", self.start, self.velocity)


class ShotOptimizer:
    def __init__(self, saucer, ship):
        self.saucer = saucer
        self.ship = ship

    @property
    def targeted_solution(self):
        if not self.ship:
            return self.random_solution
        shooter_position = self.saucer.position
        safe_distance = self.saucer.missile_head_start
        target_position = self.choose_aiming_point(safe_distance, shooter_position)
        return FiringSolution(target_position, shooter_position, safe_distance)

    def choose_aiming_point(self, safe_distance, shooter_position):
        initial_aiming_point = self.closest_aiming_point(shooter_position, self.ship.position, u.SCREEN_SIZE)
        improved_aiming_point = self.lead_the_target(initial_aiming_point, safe_distance, shooter_position)
        return improved_aiming_point

    @property
    def random_solution(self):
        return FiringSolution(self.random_position(), self.saucer.position, self.saucer.missile_head_start)

    def lead_the_target(self, target_position, safe_distance, shooter_position):
        aim_improver = AimImprover(target_position, self.ship.velocity, shooter_position, u.MISSILE_SPEED,
                                   safe_distance)
        for _ in range(3):
            target_position = aim_improver.refine_aiming_point(target_position)
        return target_position

    def random_position(self):
        return Vector2(self.random_coordinate(), self.random_coordinate())

    @staticmethod
    def random_coordinate():
        return random.randrange(0, u.SCREEN_SIZE)

    def closest_aiming_point(self, shooter_position, target_position, wrap_size):
        nearest_x = self.nearest(shooter_position.x, target_position.x, wrap_size)
        nearest_y = self.nearest(shooter_position.y, target_position.y, wrap_size)
        return Vector2(nearest_x, nearest_y)

    @staticmethod
    def nearest(shooter_coord, target_coord, screen_size):
        #     Handy Diagram
        #  ______|______|______
        #   T      T---S++T
        # Central T is more than half screen away:
        # Too far.
        # We are to his right, so
        # we shoot toward the right!
        direct_distance = abs(target_coord - shooter_coord)
        if direct_distance <= screen_size / 2:
            return target_coord
        elif shooter_coord > target_coord:
            return target_coord + screen_size
        else:
            return target_coord - screen_size

