from pygame import Vector2
from math import copysign
import u


class MovableLocation:
    def __init__(self, position, velocity, size=u.SCREEN_SIZE):
        self.position = position
        self.velocity = velocity
        self.screen_size = size

    def accelerate_by(self, acceleration_vector):
        self.velocity = self.velocity + acceleration_vector

    def accelerate_to(self, velocity):
        self.velocity = velocity

    def distance_to(self, location):
        return self.position.distance_to(location.position)

    def move(self, delta_time):
        raw_position = self.position + self.velocity*delta_time
        self.position = self.wrap_around(raw_position)
        return raw_position.x != self.position.x, raw_position.y != self.position.y

    def moving_away_from(self, vector):
        offset = self.position - vector
        sx = copysign(1, offset.x)
        sy = copysign(1, offset.y)
        vx = copysign(1, self.velocity.x)
        vy = copysign(1, self.velocity.y)
        return sx == vx or sy == vy

    def wrap_around(self, raw_position):
        return Vector2(raw_position.x % self.screen_size, raw_position.y % self.screen_size)

    def move_to(self, vector):
        self.position = vector

    def stereo_right(self):
        return self.position.x/u.SCREEN_SIZE

