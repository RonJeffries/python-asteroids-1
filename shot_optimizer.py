import random

from pygame import Vector2
import u
from missile import Missile
from time_to_target import TimeToTarget


class FiringSolution:
    def __init__(self, target_position, shooter_position, safe_distance, speed_adjustment):
        direction_to_target = (target_position - shooter_position).normalize()
        safety_offset = direction_to_target * safe_distance
        self.velocity = direction_to_target * u.MISSILE_SPEED * speed_adjustment
        self.start = shooter_position + safety_offset

    def saucer_missile(self):
        return Missile.from_saucer(self.start, self.velocity)


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
        target_position = best_target_position
        for _ in range(3):
            target_position = self.aiming_point(
                target_position,
                self.ship.velocity,
                best_target_position,
                shooter_position,
                u.MISSILE_SPEED,
                safe_distance)
        return FiringSolution(target_position, shooter_position, safe_distance, 1)

    @property
    def random_solution(self):
        return FiringSolution(self.random_position(), self.saucer.position, self.saucer.missile_head_start, 1)

    @staticmethod
    def aiming_point(target_pos, target_velocity, ship_pos, gunner_pos, missile_speed, missile_offset):
        distance = target_pos.distance_to(gunner_pos)
        time = (distance - missile_offset) / missile_speed
        target_move = time * target_velocity
        new_target_pos = ship_pos + target_move
        return new_target_pos

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

    def optimal_shot(self, delta_position, delta_velocity, initial_offset):
        aim_time = TimeToTarget(delta_position, delta_velocity).time
        adjustment_ratio = self.velocity_adjustment(aim_time, initial_offset)
        return aim_time, adjustment_ratio

    def velocity_adjustment(self, aim_time, initial_offset):
        return self.compensate_for_offset(aim_time, initial_offset) if aim_time else 1

    @staticmethod
    def compensate_for_offset(aim_time, initial_offset):
        distance_to_target = aim_time * u.MISSILE_SPEED
        adjusted_distance = distance_to_target - initial_offset
        return adjusted_distance / distance_to_target
