# Mover
import u


class Mover:
    def __init__(self, position, velocity):
        self.position = position.copy()
        self.velocity = velocity.copy()

    def accelerate_by(self, accel):
        self.velocity = self.velocity + accel

    def move(self, deltaTime):
        position = self.position + self.velocity * deltaTime
        position.x = position.x % u.SCREEN_SIZE
        position.y = position.y % u.SCREEN_SIZE
        self.position = position
