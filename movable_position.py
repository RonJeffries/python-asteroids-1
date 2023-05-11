

class MovablePosition:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def move(self, delta_time):
        self.position += self.velocity*delta_time
