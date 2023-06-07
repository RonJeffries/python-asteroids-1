import itertools

from pygame import Vector2

import u
from asteroid import Asteroid
from explosion import Explosion
from flyer import Flyer
from game_over import GameOver
from interactor import Interactor
from fragment import Fragment
from missile import Missile
from saucer import Saucer, nearest, nearest_point
from score import Score
from ship import Ship
from game import Game
from fleets import Fleets
from scorekeeper import ScoreKeeper
from wavemaker import WaveMaker


class FleetsInspector:
    def __init__(self, fleets):
        self.fleets = fleets

    def select(self, condition):
        return self.fleets.select(condition)

    @property
    def asteroids(self):
        return self.select(lambda a: isinstance(a, Asteroid))

    @property
    def explosions(self):
        return self.select(lambda a: isinstance(a, Explosion))


    @property
    def fragments(self):
        return self.select(lambda f: isinstance(f, Fragment))

    @property
    def game_over(self):
        return self.select(lambda game_over: isinstance(game_over, GameOver))

    @property
    def missiles(self):
        return self.select(lambda m: isinstance(m, Missile))

    @property
    def saucers(self):
        return self.select(lambda s: isinstance(s, Saucer))

    @property
    def saucer_missiles(self):
        return self.select(lambda m: isinstance(m, Missile) and m.is_saucer_missile)

    @property
    def scorekeeper(self):
        keepers = self.select(lambda s: isinstance(s, ScoreKeeper))
        if keepers:
            return keepers[0]
        else:
            return ScoreKeeper()

    @property
    def score(self):
        return self.scorekeeper.score

    @property
    def ships(self):
        return self.select(lambda s: isinstance(s, Ship))

    def clear_saucer_missiles(self):
        for m in self.saucer_missiles:
            self.fleets.remove_flyer(m)


FI = FleetsInspector


class BeginChecker(Flyer):
    def __init__(self):
        self.triggered = False

    def tick(self, delta_time, fleets):
        pass

    def draw(self, screen):
        pass

    def interact_with(self, other, fleets):
        pass

    def begin_interactions(self, fleets):
        self.triggered = True


class EndChecker(Flyer):
    def __init__(self):
        self.triggered = False

    def tick(self, delta_time, fleets):
        pass

    def draw(self, screen):
        pass

    def interact_with(self, other, fleets):
        pass

    def end_interactions(self, fleets):
        self.triggered = True


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

    def test_score_list(self):
        ship = Ship(u.CENTER)
        assert ship.scores_for_hitting_asteroid() == [0, 0, 0]
        missile = Missile.from_ship(u.CENTER, Vector2(0, 0))
        assert missile.scores_for_hitting_asteroid() == [100, 50, 20]
        saucer = Saucer()
        assert saucer.scores_for_hitting_asteroid() == [0, 0, 0]

    def test_missile_v_missile(self):
        pos = Vector2(100, 100)
        zero_vel = Vector2(0, 0)
        m1 = Missile.from_ship(pos, zero_vel)
        m2 = Missile.from_saucer(pos, zero_vel)
        fleets = Fleets()
        fi = FI(fleets)
        fleets.add_flyer(m1)
        fleets.add_flyer(m2)
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        assert not fi.missiles
        assert not fi.saucer_missiles

    def test_missile_asteroid_scores(self):
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        asteroids = [asteroid]
        missile = Missile.from_ship(pos, Vector2(0, 0))
        missiles = [missile]
        fleets = Fleets(asteroids, missiles, [], [], [])
        fi = FI(fleets)
        fleets.add_flyer(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        assert not fi.missiles
        assert fi.score == 20
        assert len(fi.asteroids) == 2

    def test_missile_asteroid_scores_with_missiles_in_others(self):
        fleets = Fleets()
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        fleets.add_flyer(asteroid)
        missile = Missile.from_ship(pos, Vector2(0, 0))
        fleets.add_flyer(missile)
        fleets.add_flyer(ScoreKeeper())
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
        ships = [ship]
        missile = Missile.from_ship(pos, Vector2(0, 0))
        missiles = [missile]
        fleets = Fleets([], missiles, [], [], ships)
        fi = FI(fleets)
        fleets.add_flyer(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        assert not fi.missiles
        assert not fi.ships
        assert fi.score == 0

    def test_asteroid_ship_does_not_score(self):
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        asteroids = [asteroid]
        ship = Ship(pos)
        ships = [ship]
        fleets = Fleets(asteroids, [], [], [], ships)
        fi = FI(fleets)
        fleets.add_flyer(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        assert not fi.ships
        assert fi.score == 0
        assert len(fi.asteroids) == 2

    def test_saucer_ship_does_not_score(self):
        pos = Vector2(100, 100)
        saucer = Saucer()
        saucer.move_to(pos)
        saucers = [saucer]
        ship = Ship(pos)
        ships = [ship]
        fleets = Fleets([], [], saucers, [], ships)
        fi = FI(fleets)
        fleets.add_flyer(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        assert not fi.ships
        assert fi.score == 0

    def test_asteroid_saucer_does_not_score(self):
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        asteroids = [asteroid]
        saucer = Saucer()
        saucer.move_to(pos)
        saucers = [saucer]
        fleets = Fleets(asteroids, [], saucers, [], [])
        fi = FI(fleets)
        fleets.add_flyer(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        assert not fi.saucers
        assert fi.score == 0
        assert len(fi.asteroids) == 2

    def test_saucer_ship_missile_scores(self):
        pos = Vector2(100, 100)
        saucer = Saucer()
        self.interact_with_missile(pos, saucer, 200)

    @staticmethod
    def interact_with_missile(pos, saucer, expected_score):
        saucer.move_to(pos)
        saucers = [saucer]
        missile = Missile.from_ship(pos, Vector2(0, 0))
        missiles = [missile]
        fleets = Fleets([], missiles, saucers, [], [])
        fi = FI(fleets)
        fleets.add_flyer(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        assert not fi.missiles
        assert not fi.saucers
        assert fi.score == expected_score
        return interactor

    def test_small_saucer_ship_missile_scores(self):
        pos = Vector2(100, 100)
        saucer = Saucer(pos, 1)
        self.interact_with_missile(pos, saucer, 1000)

    def test_saucer_vs_saucer_missile_does_not_score(self):
        pos = Vector2(100, 100)
        saucer = Saucer()
        saucer.move_to(pos)
        saucers = [saucer]
        missile = Missile.from_saucer(pos, Vector2(0, 0))
        missiles = [missile]
        fleets = Fleets([], missiles, saucers, [], [])
        fi = FI(fleets)
        fleets.add_flyer(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        interactor.perform_interactions()
        assert not fi.missiles
        assert not fi.saucers
        assert fi.score == 0

    def test_everyone_supports_asteroid_score_lists(self):
        asteroid = Asteroid()
        missile = Missile.from_ship(Vector2(100, 100), Vector2(100, 100))
        saucer = Saucer()
        ship = Ship(Vector2(200, 200))
        assert asteroid.scores_for_hitting_asteroid()
        assert missile.scores_for_hitting_asteroid()
        assert saucer.scores_for_hitting_asteroid()
        assert ship.scores_for_hitting_asteroid()

    def test_everyone_supports_saucer_score_lists(self):
        asteroid = Asteroid()
        missile = Missile.from_ship(Vector2(100, 100), Vector2(100, 100))
        saucer = Saucer()
        ship = Ship(Vector2(200, 200))
        assert asteroid.scores_for_hitting_saucer()
        assert missile.scores_for_hitting_saucer()
        assert saucer.scores_for_hitting_saucer()
        assert ship.scores_for_hitting_saucer()

    def test_create_asteroid_at_zero(self):
        asteroid = Asteroid(2, Vector2(0, 0))
        assert asteroid.position == Vector2(0, 0)

    def test_collider(self):
        fleets = Fleets([], [], [], [], [])
        fleets.add_flyer(ScoreKeeper())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        assert FI(fleets).score == 0

    def test_begin_end(self):
        begin = BeginChecker()
        end = EndChecker()
        assert not begin.triggered
        assert not end.triggered
        asteroids = [begin, end]
        interactor = Interactor(Fleets(asteroids))
        interactor.perform_interactions()
        assert begin.triggered
        assert end.triggered

    def test_collider_via_game_with_score(self):
        game = Game(True)
        asteroid = Asteroid(2, Vector2(100, 100))
        game.fleets.add_flyer(asteroid)
        game.fleets.add_flyer(ScoreKeeper())
        missile = Missile.from_ship(Vector2(100, 100), Vector2(3, 3))
        game.fleets.add_flyer(missile)
        game.perform_interactions()
        game.perform_interactions()
        assert FI(game.fleets).score == 20

    def test_cached_collider_is_safe(self):
        asteroid = Asteroid(2, Vector2(100, 100))
        missile = Missile.from_ship(Vector2(100, 100), Vector2(3, 3))
        asteroids = [asteroid]
        missiles = [missile]
        fleets = Fleets(asteroids, missiles, [], [], [])
        fi = FI(fleets)
        fleets.add_flyer(ScoreKeeper())
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
        assert nearest(shooter, target, screen_size) == 100
        shooter = 400
        assert nearest(shooter, target, screen_size) == 100 + 500
        target = 400
        shooter = 100
        assert nearest(shooter, target, screen_size) == 400 - 500

    def test_can_choose_nearest_point(self):
        target = Vector2(100, 400)
        screen_size = 500
        shooter = Vector2(150, 150)
        assert nearest_point(shooter, target, screen_size) == Vector2(100, 400)
        shooter = Vector2(150, 50)
        assert nearest_point(shooter, target, screen_size) == Vector2(100, -100)

    def test_flyer_protocol(self):
        classes = [Asteroid, Missile, Saucer, Ship, Fragment, Score, ScoreKeeper]
        errors = []
        for klass in classes:
            assert issubclass(klass, Flyer)
            attrs = dir(klass)
            methods = ["interact_with",
                       "interact_with_asteroid",
                       "interact_with_missile",
                       "interact_with_saucer",
                       "interact_with_ship",
                       "interact_with_score",
                       "interact_with_scorekeeper",
                       "are_we_colliding",
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
        m_ship = Missile.from_ship(Vector2(0, 0), Vector2(0, 0))
        m_saucer = Missile.from_saucer(Vector2(0, 0), Vector2(0, 0))
        ship.interact_with_missile(m_ship, fleets)
        ship.interact_with_missile(m_saucer, fleets)
        assert ship._missile_tally == 1

    def test_fleets_select(self):
        fleets = Fleets()
        fleets.add_flyer(Asteroid(2))
        fleets.add_flyer(Asteroid(1))
        fleets.add_flyer(WaveMaker())
        wm = fleets.select(lambda x: isinstance(x, WaveMaker))
        assert len(wm) == 1
        as2 = fleets.select(lambda x: isinstance(x, Asteroid))
        assert len(as2) == 2
        as1 = fleets.select(lambda x: isinstance(x, Asteroid) and x.size == 2)
        assert len(as1) == 1
