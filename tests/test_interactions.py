import itertools

from pygame import Vector2

import u
from asteroids.asteroid import Asteroid
from core.fleets import Fleets
from flyer import AsteroidFlyer
from asteroids.fragment import Fragment
from core.game import Game
from core.interactor import Interactor
from asteroids.missile import Missile
from asteroids.saucer import Saucer
from asteroids.score import Score
from asteroids.scorekeeper import ScoreKeeper
from asteroids.ship import Ship
from asteroids.shot_optimizer import ShotOptimizer
from tests.tools import FI, BeginChecker, EndChecker
from asteroids.wavemaker import WaveMaker


class TestInteractions:
    def test_firing_limit(self):
        ship = Ship(u.CENTER)
        missile_count = 0
        fleets = Fleets()
        for i in range(5):
            missile_count = self.attempt_fire(fleets, ship)
        assert missile_count == u.MISSILE_LIMIT
        missile_count = self.attempt_fire(fleets, ship)
        assert missile_count == u.MISSILE_LIMIT

    @staticmethod
    def attempt_fire(fleets, ship):
        ship._can_fire = True
        ship._missile_tally = 0
        for flyer in fleets.all_objects:
            flyer.interact_with(ship, fleets)
        ship.fire_if_possible(fleets, )
        missile_count = len([m for m in fleets.all_objects])
        return missile_count

    def test_missile_v_missile(self):
        pos = Vector2(100, 100)
        zero_vel = Vector2(0, 0)
        m1 = Missile("ship", pos, zero_vel)
        m2 = Missile("saucer", pos, zero_vel)
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(m1)
        fleets.append(m2)
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        assert not fi.missiles

    def test_missile_v_asteroid(self):
        pos = Vector2(100, 100)
        zero_vel = Vector2(0, 0)
        missile = Missile("ship", pos, zero_vel)
        asteroid = Asteroid(2, pos)
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(missile)
        fleets.append(asteroid)
        fleets.perform_interactions()
        assert not fi.missiles
        assert len(fi.asteroids) == 2

    def test_saucer_missile_v_asteroid(self):
        pos = Vector2(100, 100)
        zero_vel = Vector2(0, 0)
        missile = Missile("saucer", pos, zero_vel)
        asteroid = Asteroid(2, pos)
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(missile)
        fleets.append(asteroid)
        fleets.perform_interactions()
        assert not fi.missiles
        assert len(fi.asteroids) == 2

    def test_missile_asteroid_scores(self):
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        missile = Missile("ship", pos, Vector2(0, 0))
        fleets = Fleets()
        fleets.append(asteroid)
        fleets.append(missile)
        fi = FI(fleets)
        fleets.append(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        assert not fi.missiles
        assert fi.score == 20
        assert len(fi.asteroids) == 2

    def test_missile_vs_asteroid_scoring(self):
        fleets = Fleets()
        fi = FI(fleets)
        pos = Vector2(100, 100)
        vel = Vector2(0, 0)
        asteroid = Asteroid(2, pos)
        missile = Missile("ship", pos, vel)
        asteroid.interact_with_missile(missile, fleets)
        scores = fi.scores
        assert scores[0].score == u.ASTEROID_SCORE_LIST[asteroid.size]
        asteroid = Asteroid(1, pos)
        asteroid.interact_with_missile(missile, fleets)
        scores = fi.scores
        assert scores[1].score == u.ASTEROID_SCORE_LIST[asteroid.size]
        asteroid = Asteroid(0, pos)
        asteroid.interact_with_missile(missile, fleets)
        scores = fi.scores
        assert scores[2].score == u.ASTEROID_SCORE_LIST[asteroid.size]

    def test_missile_only_scores_on_hit(self):
        # yes there was such a defect for a moment
        fleets = Fleets()
        fi = FI(fleets)
        ship_pos = Vector2(100, 100)
        asteroid_pos = Vector2(900, 900)
        vel = Vector2(0, 0)
        asteroid = Asteroid(2, asteroid_pos)
        missile = Missile("ship", ship_pos, vel)
        asteroid.interact_with_missile(missile, fleets)
        assert not fi.scores

    def test_missile_scores_two_asteroids_at_once(self):
        fleets = Fleets()
        fi = FI(fleets)
        pos = Vector2(100, 100)
        vel = Vector2(0, 0)
        expected = u.ASTEROID_SCORE_LIST[2] + u.ASTEROID_SCORE_LIST[1]
        asteroid1 = Asteroid(2, pos)
        asteroid2 = Asteroid(1, pos)
        missile = Missile("ship", pos, vel)
        keeper = ScoreKeeper()
        fleets.append(asteroid1)
        fleets.append(asteroid2)
        fleets.append(missile)
        fleets.append(keeper)
        fleets.perform_interactions()
        assert len(fi.asteroids) == 4
        assert len(fi.scores) == 2
        fleets.perform_interactions()
        assert fi.score == expected

    def test_missile_asteroid_scores_with_missiles_in_others(self):
        fleets = Fleets()
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        fleets.append(asteroid)
        missile = Missile("ship", pos, Vector2(0, 0))
        fleets.append(missile)
        fleets.append(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        missiles = FI(fleets).missiles
        assert not missiles
        assert FI(fleets).score == 20
        asteroids = FI(fleets).asteroids
        assert len(asteroids) == 2

    def test_missile_ship_does_not_score(self):
        pos = Vector2(100, 100)
        ship = Ship(pos)
        missile = Missile("ship", pos, Vector2(0, 0))
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(ship)
        fleets.append(missile)
        fleets.append(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        assert not fi.missiles
        assert not fi.ships
        assert fi.score == 0

    def test_asteroid_ship_does_not_score(self):
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        ship = Ship(pos)
        fleets = Fleets()
        fleets.append(ship)
        fleets.append(asteroid)
        fi = FI(fleets)
        fleets.append(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        assert not fi.ships
        assert fi.score == 0
        assert len(fi.asteroids) == 2

    def test_saucer_ship_does_not_score(self):
        pos = Vector2(100, 100)
        saucer = Saucer.large()
        saucer.move_to(pos)
        ship = Ship(pos)
        fleets = Fleets()
        fleets.append(saucer)
        fleets.append(ship)
        fi = FI(fleets)
        assert fi.ships
        fleets.append(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        assert not fi.ships
        assert fi.score == 0

    def test_asteroid_saucer_does_not_score(self):
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        saucer = Saucer.large()
        saucer.move_to(pos)
        fleets = Fleets()
        fleets.append(asteroid)
        fleets.append(saucer)
        fi = FI(fleets)
        fleets.append(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        assert not fi.saucers
        assert fi.score == 0
        assert len(fi.asteroids) == 2

    def test_saucer_ship_missile_scores(self):
        pos = Vector2(100, 100)
        saucer = Saucer.large()
        self.interact_with_missile(pos, saucer, 200)

    @staticmethod
    def interact_with_missile(pos, saucer, expected_score):
        saucer.move_to(pos)
        missile = Missile("ship", pos, Vector2(0, 0))
        fleets = Fleets()
        fleets.append(saucer)
        fleets.append(missile)
        fi = FI(fleets)
        fleets.append(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        assert not fi.missiles
        assert not fi.saucers
        assert fi.score == expected_score
        return interactor

    def test_small_saucer_ship_missile_scores(self):
        pos = Vector2(100, 100)
        saucer = Saucer.small()
        self.interact_with_missile(pos, saucer, 1000)

    def test_saucer_vs_saucer_missile_does_not_score(self):
        pos = Vector2(100, 100)
        saucer = Saucer.large()
        saucer.move_to(pos)
        missile = Missile("saucer", pos, Vector2(0, 0))
        fleets = Fleets()
        fleets.append(saucer)
        fleets.append(missile)
        fi = FI(fleets)
        assert fi.missiles
        assert fi.saucers
        fleets.append(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        assert not fi.missiles
        assert not fi.saucers
        assert fi.score == 0

    def test_create_asteroid_at_zero(self):
        asteroid = Asteroid(2, Vector2(0, 0))
        assert asteroid.position == Vector2(0, 0)

    def test_collider(self):
        fleets = Fleets()
        fleets.append(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        assert FI(fleets).score == 0

    def test_begin_end(self):
        begin = BeginChecker()
        end = EndChecker()
        assert not begin.triggered
        assert not end.triggered
        fleets = Fleets()
        fleets.append(begin)
        fleets.append(end)
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        assert begin.triggered
        assert end.triggered

    def test_collider_via_game_with_score(self):
        game = Game(True)
        asteroid = Asteroid(2, Vector2(100, 100))
        game.fleets.append(asteroid)
        game.fleets.append(ScoreKeeper())
        missile = Missile("ship", Vector2(100, 100), Vector2(3, 3))
        game.fleets.append(missile)
        game.fleets.perform_interactions()
        game.fleets.perform_interactions()
        assert FI(game.fleets).score == 20

    def test_cached_collider_is_safe(self):
        asteroid = Asteroid(2, Vector2(100, 100))
        missile = Missile("ship", Vector2(100, 100), Vector2(3, 3))
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(asteroid)
        fleets.append(missile)
        fleets.append(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        assert fi.score == 20
        interactor.perform_interactions()
        assert fi.score == 20

    def test_can_choose_nearest_scalar_target(self):
        target = 100
        screen_size = 500
        shooter = 200
        assert ShotOptimizer.nearest(shooter, target, screen_size) == 100
        shooter = 400
        assert ShotOptimizer.nearest(shooter, target, screen_size) == 100 + 500
        target = 400
        shooter = 100
        assert ShotOptimizer.nearest(shooter, target, screen_size) == 400 - 500

    def test_can_choose_nearest_point(self):
        target = Vector2(100, 400)
        ship = Ship(target)
        screen_size = 500
        shooter = Vector2(150, 150)
        saucer = Saucer.large()
        saucer.move_to(shooter)
        gunner = ShotOptimizer(saucer, ship)
        assert gunner.closest_aiming_point(shooter, target, screen_size) == Vector2(100, 400)
        shooter = Vector2(150, 50)
        assert gunner.closest_aiming_point(shooter, target, screen_size) == Vector2(100, -100)

    def test_flyer_protocol(self):
        classes = [Asteroid, Missile, Saucer, Ship, Fragment, Score, ScoreKeeper]
        errors = []
        for klass in classes:
            assert issubclass(klass, AsteroidFlyer)
            attrs = dir(klass)
            methods = ["interact_with",
                       "interact_with_asteroid",
                       "interact_with_missile",
                       "interact_with_saucer",
                       "interact_with_ship",
                       "interact_with_score",
                       "interact_with_scorekeeper",
                       "tick",
                       "draw"]
            for method in methods:
                if method not in attrs:
                    errors.append((klass.__name__, method))
        assert not errors

    def test_combinations_handles_delete(self):
        # combinations seems to create a protected tuple
        numbers = [1, 2, 3]
        total = 0
        for a, b in itertools.combinations(numbers, 2):
            total = total + a + b
        assert total == 12
        total = 0
        for a, b in itertools.combinations(numbers, 2):
            if a in numbers:
                numbers.remove(a)
            if b in numbers:
                numbers.remove(b)
            total = total + a + b
        assert total == 12
        assert not numbers

    def test_ship_counts_missiles(self):
        fleets = Fleets()
        ship = Ship(u.CENTER)
        ship.begin_interactions(fleets)
        m_ship = Missile("ship", Vector2(0, 0), Vector2(0, 0))
        m_saucer = Missile("saucer", Vector2(0, 0), Vector2(0, 0))
        ship.interact_with_missile(m_ship, fleets)
        ship.interact_with_missile(m_saucer, fleets)
        assert ship._missile_tally == 1

    def test_fleets_select(self):
        fleets = Fleets()
        fleets.append(Asteroid(2))
        fleets.append(Asteroid(1))
        fleets.append(WaveMaker())
        wm = fleets.select(lambda x: isinstance(x, WaveMaker))
        assert len(wm) == 1
        as2 = fleets.select(lambda x: isinstance(x, Asteroid))
        assert len(as2) == 2
        as1 = fleets.select(lambda x: isinstance(x, Asteroid) and x.size == 2)
        assert len(as1) == 1
