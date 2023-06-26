import math

import u


class ShotOptimizer:
    def __init__(self, delta_position, delta_velocity, initial_offset):
        self.aim_time, self.adjustment_ratio = self.optimal_shot(delta_position, delta_velocity, initial_offset)

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
        # return time for hit or -1
        # quadratic
        a = relative_velocity.dot(relative_velocity) - u.MISSILE_SPEED*u.MISSILE_SPEED
        b = 2 * relative_velocity.dot(delta_position)
        c = delta_position.dot(delta_position)
        disc = b*b - 4*a*c
        if disc < 0:
            return 0
        else:
            divisor = (math.sqrt(disc) - b)
            if divisor:
                return 2*c / divisor
            else:
                return 0
