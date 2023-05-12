import u


class MovableLocation:
    def __init__(self, position, velocity, size=u.SCREEN_SIZE):
        self.position = position
        self.velocity = velocity
        self.size = size

    def move(self, delta_time):
        position = self.position + self.velocity*delta_time
        position.x = position.x % self.size
        position.y = position.y % self.size
        self.position = position

