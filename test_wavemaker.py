import u
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

