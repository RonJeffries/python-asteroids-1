import u


class MovableLocation:
    def __init__(self, position, velocity, size=u.SCREEN_SIZE):
        self.position = position
        self.velocity = velocity
        self.size = size

    def accelerate_by(self, acceleration_vector):
        self.velocity = self.velocity + acceleration_vector

    def move(self, delta_time):
        position = self.position + self.velocity*delta_time
        old_x = position.x
        old_y = position.y
        position.x = position.x % self.size
        position.y = position.y % self.size
        self.position = position
        return position.x != old_x, position.y != old_y

    def move_to(self, vector):
        self.position = vector

