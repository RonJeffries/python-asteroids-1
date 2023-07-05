import random

from pygame import Vector2
import u
from missile import Missile


class FiringSolution:
    def __init__(self, target_position, shooter_position, safe_distance, speed_adjustment):
        direction_to_target = (target_position - shooter_position).normalize()
        safety_offset = direction_to_target * safe_distance
        self.velocity = direction_to_target * u.MISSILE_SPEED * speed_adjustment
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
        best_target_position = self.closest_aiming_point(shooter_position, self.ship.position, u.SCREEN_SIZE)
        vector_to_target = best_target_position - shooter_position
        safe_distance = self.saucer.missile_head_start
        target_position = self.lead_the_target(best_target_position, safe_distance, shooter_position)
        return FiringSolution(target_position, shooter_position, safe_distance, 1)

    def lead_the_target(self, best_target_position, safe_distance, shooter_position):
        target_position = best_target_position
        for _ in range(3):
            target_position = self.improved_aiming_point(
                target_position,
                self.ship.velocity,
                best_target_position,
                shooter_position,
                u.MISSILE_SPEED,
                safe_distance)
        return target_position

    @property
    def random_solution(self):
        return FiringSolution(self.random_position(), self.saucer.position, self.saucer.missile_head_start, 1)

    @staticmethod
    def improved_aiming_point(
            initial_aiming_point,
            target_velocity,
            target_starting_position,
            gunner_position,
            missile_speed,
            missile_offset):
        missile_travel_distance = gunner_position.distance_to(initial_aiming_point) - missile_offset
        missile_travel_time = missile_travel_distance / missile_speed
        target_motion = missile_travel_time * target_velocity
        better_aiming_point = target_starting_position + target_motion
        return better_aiming_point

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
        # Central T is too far away.
        # We are to his right, so
        # we shoot toward the right!
        direct_distance = abs(target_coord - shooter_coord)
        if direct_distance <= screen_size / 2:
            return target_coord
        elif shooter_coord > target_coord:
            return target_coord + screen_size
        else:
            return target_coord - screen_size

