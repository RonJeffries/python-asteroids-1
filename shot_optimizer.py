import math
from pygame import Vector2
import u


class FiringSolution:
    def __init__(self, target_position, shooter_position, safe_distance, speed_adjustment):
        direction_to_target = (target_position - shooter_position).normalize()
        safety_offset = direction_to_target * safe_distance
        self.velocity = direction_to_target * u.MISSILE_SPEED * speed_adjustment
        self.start = shooter_position + safety_offset


class ShotOptimizer:
    def __init__(self, saucer, ship):
        shooter_position = saucer.position
        best_target_position = self.closest_aiming_point(shooter_position, ship.position, u.SCREEN_SIZE)
        vector_to_target = best_target_position - shooter_position
        safe_distance = saucer.missile_head_start
        aim_time, speed_adjustment = self.optimal_shot(vector_to_target, ship.velocity, safe_distance)
        target_position = best_target_position + ship.velocity * aim_time

        solution = FiringSolution(target_position, shooter_position, safe_distance, speed_adjustment)

        self.velocity = solution.velocity
        self.start = solution.start

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


class TimeToTarget:
    def __init__(self, delta_position, relative_velocity):
        # from https://www.gamedeveloper.com/programming/shooting-a-moving-target#close-modal
        # return time for hit or 0
        # quadratic
        # Quadratic equation coefficients a*t^2 + b*t + c = 0
        a = relative_velocity.dot(relative_velocity) - u.MISSILE_SPEED*u.MISSILE_SPEED
        b = 2 * relative_velocity.dot(delta_position)
        c = delta_position.dot(delta_position)
        self.result = self.quadratic_formula(a, b, c)

    def quadratic_formula(self, a, b, c):
        disc = b*b - 4*a*c
        return 0 if disc < 0 else self.calculate(b, c, disc)

    def calculate(self, b, c, disc):
        divisor = (math.sqrt(disc) - b)
        return 0 if divisor == 0 else 2 * c / divisor

    @property
    def time(self):
        return self.result
