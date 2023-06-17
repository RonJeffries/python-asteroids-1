import u
from asteroid import Asteroid
from flyer import Flyer
from timer import Timer


class WaveMaker(Flyer):

    def __init__(self):
        self._need_asteroids = None
        self._timer = Timer(u.ASTEROID_DELAY)
        self._number_to_create = 2

    def create_asteroids(self, fleets):
        self._number_to_create += 2
        if self._number_to_create > 11:
            self._number_to_create = 11
        for i in range(self._number_to_create):
            fleets.append(Asteroid())

    def begin_interactions(self, fleets):
        self._need_asteroids = True

    def interact_with_asteroid(self, asteroid, fleets):
        self._need_asteroids = False

    def interact_with_explosion(self, explosion, fleets):
        pass

    def interact_with_fragment(self, fragment, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucermissile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass

    def tick(self, delta_time, fleets):
        if self._need_asteroids:
            self._timer.tick(delta_time, self.create_asteroids, fleets)

    def interact_with(self, other, fleets):
        other.interact_with_wavemaker(self, fleets)

    def draw(self, screen):
        pass
