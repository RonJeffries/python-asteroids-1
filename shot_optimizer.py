import math

from pygame import Vector2

import u


class ShotOptimizer:
    def __init__(self, saucer, ship):
        best_target_position = self.closest_aiming_point(saucer.position, ship.position, u.SCREEN_SIZE)
        vector_to_target = best_target_position - saucer.position
        safe_distance = saucer.missile_head_start
        aim_time, speed_adjustment = self.optimal_shot(vector_to_target, ship.velocity, safe_distance)
        future_target_position = best_target_position + ship.velocity * aim_time

        direction_to_target = (future_target_position - saucer.position).normalize()
        safety_offset = direction_to_target * safe_distance
        velocity = direction_to_target * u.MISSILE_SPEED * speed_adjustment
        start = saucer.position + safety_offset

        self.velocity = velocity
        self.start = start

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
        aim_time = self.time_to_target(delta_position, delta_velocity)
        adjustment_ratio = self.velocity_adjustment(aim_time, initial_offset)
        return aim_time, adjustment_ratio

    def velocity_adjustment(self, aim_time, initial_offset):
        return self.compensate_for_offset(aim_time, initial_offset) if aim_time else 1

    @staticmethod
    def compensate_for_offset(aim_time, initial_offset):
        distance_to_target = aim_time * u.MISSILE_SPEED
        adjusted_distance = distance_to_target - initial_offset
        return adjusted_distance / distance_to_target

    @staticmethod
    def time_to_target(delta_position, relative_velocity):
        # from https://www.gamedeveloper.com/programming/shooting-a-moving-target#close-modal
        # return time for hit or 0
        # quadratic
        a = relative_velocity.dot(relative_velocity) - u.MISSILE_SPEED*u.MISSILE_SPEED
        b = 2 * relative_velocity.dot(delta_position)
        c = delta_position.dot(delta_position)
        disc = b*b - 4*a*c
        if disc < 0:
            return 0
        divisor = (math.sqrt(disc) - b)
        if divisor == 0:
            return 0
        return 2*c / divisor
