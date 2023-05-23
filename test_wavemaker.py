import u
from asteroid import Asteroid
from fleets import Fleets
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

    def interact_with(self, other, fleets):
        pass

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleet, fleets):
        if not self.saw_asteroids:
            self.timer.tick(delta_time, fleets)


class TestWaveMaker:
    def test_detects_asteroids(self):
        fleets = Fleets()
        maker = WaveMaker()
        maker.begin_interactions(fleets)
        assert not maker.saw_asteroids
        maker.interact_with_asteroid(None, fleets)
        assert maker.saw_asteroids

    def test_timer(self):
        fleets = Fleets()
        maker = WaveMaker()
        maker.begin_interactions(fleets)
        assert not maker.saw_asteroids
        assert not fleets.asteroid_count
        maker.tick(0.1, None, fleets)
        assert not fleets.asteroid_count
        maker.tick(u.ASTEROID_DELAY, None, fleets)
        assert fleets.asteroid_count == 4
        for asteroid in fleets.asteroids:
            fleets.remove_asteroid(asteroid)
        maker.begin_interactions(fleets)
        maker.tick(0.1, None, fleets)
        assert not fleets.asteroid_count
        maker.tick(u.ASTEROID_DELAY, None, fleets)
        assert fleets.asteroid_count == 6

