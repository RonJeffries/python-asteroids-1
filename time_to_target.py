import math

import u


class TimeToTarget:
    def __init__(self, delta_position, relative_velocity):
        # from https://www.gamedeveloper.com/programming/shooting-a-moving-target#close-modal
        # return time for hit or 0
        # quadratic
        # Quadratic equation coefficients a*t^2 + b*t + c = 0
        a = relative_velocity.dot(relative_velocity) - u.MISSILE_SPEED*u.MISSILE_SPEED
        b = 2 * relative_velocity.dot(delta_position)
        c = delta_position.dot(delta_position)
        self.result = quadratic_formula(a, b, c)

    @property
    def time(self):
        return self.result


def calculate(b, c, disc):
    divisor = (math.sqrt(disc) - b)
    return 2 * c / divisor if divisor != 0 else 0


def quadratic_formula(a, b, c):
    disc = b*b - 4*a*c
    return calculate(b, c, disc) if disc >= 0 else 0