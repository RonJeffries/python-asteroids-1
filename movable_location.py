from pygame import Vector2

import u


class MovableLocation:
    def __init__(self, position, velocity, size=u.SCREEN_SIZE):
        self.position = position
        self.velocity = velocity
        self.size = size

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

    def wrap_around(self, raw_position):
        return Vector2(raw_position.x % self.size, raw_position.y % self.size)

    def move_to(self, vector):
        self.position = vector

    def stereo_right(self):
        return self.position.x/u.SCREEN_SIZE

