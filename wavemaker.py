import u
from asteroid import Asteroid
from flyer import Flyer
from timer import Timer


class WaveMaker(Flyer):
    def __init__(self):
        self.saw_asteroids = None
        self.timer = Timer(u.ASTEROID_DELAY, self.create_asteroids)
        self.asteroid_count = 2

    def create_asteroids(self, fleets):
        self.asteroid_count += 2
        if self.asteroid_count > 11:
            self.asteroid_count = 11
        for i in range(self.asteroid_count):
            fleets.add_asteroid(Asteroid())

    def begin_interactions(self, fleets):
        self.saw_asteroids = False

    def interact_with_asteroid(self, asteroid, fleets):
        self.saw_asteroids = True

    def tick(self, delta_time, fleet, fleets):
        if not self.saw_asteroids:
            self.timer.tick(delta_time, fleets)

    def interact_with(self, other, fleets):
        pass

    def draw(self, screen):
        pass
