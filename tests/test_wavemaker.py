import u
from asteroids.asteroid import Asteroid
from core.fleets import Fleets
from asteroids.wavemaker import WaveMaker


class TestWaveMaker:
    def test_detects_asteroids(self):
        fleets = Fleets()
        maker = WaveMaker()
        maker.begin_interactions(fleets)
        assert maker._need_asteroids
        maker.interact_with_asteroid(None, fleets)
        assert not maker._need_asteroids

    def test_timer(self):
        fleets = Fleets()
        maker = WaveMaker()
        maker.begin_interactions(fleets)
        assert maker._need_asteroids
        assert not self.count_asteroids(fleets)
        maker.tick(0.1, fleets)
        assert not self.count_asteroids(fleets)
        maker.tick(u.ASTEROID_DELAY, fleets)
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
    def find_asteroids(fleets):
        return [a for a in fleets.all_objects if isinstance(a, Asteroid)]

    def count_asteroids(self, fleets):
        asteroids = self.find_asteroids(fleets)
        return len(asteroids)

    def clear_and_tick(self, fleets, maker):
        for asteroid in self.find_asteroids(fleets):
            fleets.remove(asteroid)
        maker.begin_interactions(fleets)
        maker.tick(0.1, fleets)
        assert not self.count_asteroids(fleets)
        maker.tick(u.ASTEROID_DELAY, fleets)


