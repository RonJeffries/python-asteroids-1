# Mover
import u


class Mover:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def move(self, deltaTime):
        self.position += self.velocity*deltaTime
        self.position.x = self.position.x % u.SCREEN_SIZE
        self.position.y = self.position.y % u.SCREEN_SIZE