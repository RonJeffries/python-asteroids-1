import u
from asteroid import Asteroid
from fleets import Fleets
from wavemaker import WaveMaker


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
        assert not self.count_asteroids(fleets)
        maker.tick(0.1, None, fleets)
        assert not self.count_asteroids(fleets)
        maker.tick(u.ASTEROID_DELAY, None, fleets)
        assert self.count_asteroids(fleets) == 4

        self.clear_and_tick(fleets, maker)
        assert self.count_asteroids(fleets) == 6

        self.clear_and_tick(fleets, maker)
        assert self.count_asteroids(fleets) == 8

        self.clear_and_tick(fleets, maker)
        assert self.count_asteroids(fleets) == 10

        self.clear_and_tick(fleets, maker)
        assert self.count_asteroids(fleets) == 11

        self.clear_and_tick(fleets, maker)
        assert self.count_asteroids(fleets) == 11

    @staticmethod
    def count_asteroids(fleets):
        asteroids = [a for a in fleets.asteroids if isinstance(a, Asteroid)]
        return len(asteroids)

    def clear_and_tick(self, fleets, maker):
        for asteroid in fleets.asteroids:
            fleets.remove_asteroid(asteroid)
        maker.begin_interactions(fleets)
        maker.tick(0.1, None, fleets)
        assert not self.count_asteroids(fleets)
        maker.tick(u.ASTEROID_DELAY, None, fleets)


