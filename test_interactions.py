import itertools

from pygame import Vector2

import u
from asteroid import Asteroid
from flyer import Flyer
from interactor import Interactor
from fleet import MissileFleet
from fragment import Fragment
from missile import Missile
from saucer import Saucer, nearest, nearest_point
from score import Score
from ship import Ship
from game import Game
from fleets import Fleets
from scorekeeper import ScoreKeeper


class BeginChecker(Flyer):
    def __init__(self):
        self.triggered = False

    def tick(self, delta_time, fleet, fleets):
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

    def tick(self, delta_time, fleet, fleets):
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
        count = 0
        missiles = MissileFleet([], u.MISSILE_LIMIT)
        while len(missiles) < u.MISSILE_LIMIT:
            ship._can_fire = True
            ship.fire_if_possible(missiles)
            count += 1
            assert len(missiles) == count
        assert len(missiles) == u.MISSILE_LIMIT
        ship._can_fire = True
        ship.fire_if_possible(missiles)
        assert len(missiles) == u.MISSILE_LIMIT

    # it's barely possible for two missiles to kill the
    # same asteroid. This used to cause a crash, trying
    # to remove the same asteroid twice.
    def test_dual_kills(self):
        asteroid = Asteroid(2, Vector2(0, 0))
        asteroids = [asteroid]
        fleets = Fleets(asteroids)
        asteroid.split_or_die(fleets)
        assert asteroid not in asteroids
        assert len(asteroids) == 2
        asteroid.split_or_die(fleets)
        assert len(asteroids) == 2  # didn't crash, didn't split again

    def test_score_list(self):
        ship = Ship(u.CENTER)
        assert ship.scores_for_hitting_asteroid() == [0, 0, 0]
        missile = Missile.from_ship(u.CENTER, Vector2(0, 0))
        assert missile.scores_for_hitting_asteroid() == [100, 50, 20]
        saucer = Saucer()
        assert saucer.scores_for_hitting_asteroid() == [0, 0, 0]

    def test_missile_asteroid_scores(self):
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        asteroids = [asteroid]
        missile = Missile.from_ship(pos, Vector2(0, 0))
        missiles = [missile]
        interactor = Interactor(Fleets(asteroids, missiles, [], [], []))
        interactor.interact_one_pair(asteroid, missile)
        assert not missiles
        assert interactor.score == 20
        assert len(asteroids) == 2

    def test_missile_ship_does_not_score(self):
        pos = Vector2(100, 100)
        ship = Ship(pos)
        ships = [ship]
        missile = Missile.from_ship(pos, Vector2(0, 0))
        missiles = [missile]
        interactor = Interactor(Fleets([], missiles, [], [], ships))
        interactor.interact_one_pair(ship, missile)
        assert not missiles
        assert not ships
        assert interactor.score == 0

    def test_asteroid_ship_does_not_score(self):
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        asteroids = [asteroid]
        ship = Ship(pos)
        ships = [ship]
        interactor = Interactor(Fleets(asteroids, [], [], [], ships))
        interactor.interact_one_pair(asteroid, ship)
        assert not ships
        assert interactor.score == 0
        assert len(asteroids) == 2

    def test_saucer_ship_does_not_score(self):
        pos = Vector2(100, 100)
        saucer = Saucer()
        saucer.move_to(pos)
        saucers = [saucer]
        ship = Ship(pos)
        interactor = [ship]
        collider = Interactor(Fleets([], [], saucers, [], interactor))
        collider.interact_one_pair(saucer, ship)
        assert not interactor
        assert collider.score == 0

    def test_asteroid_saucer_does_not_score(self):
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        asteroids = [asteroid]
        saucer = Saucer()
        saucer.move_to(pos)
        saucers = [saucer]
        interactor = Interactor(Fleets(asteroids, [], saucers, [], []))
        interactor.interact_one_pair(asteroid, saucer)
        assert not saucers
        assert interactor.score == 0
        assert len(asteroids) == 2

    def test_saucer_ship_missile_scores(self):
        pos = Vector2(100, 100)
        saucer = Saucer()
        interactor = self.destroy_each_other(pos, saucer)
        assert interactor.score == 200

    def destroy_each_other(self, pos, saucer):
        saucer.move_to(pos)
        saucers = [saucer]
        missile = Missile.from_ship(pos, Vector2(0, 0))
        missiles = [missile]
        interactor = Interactor(Fleets([], missiles, saucers, [], []))
        interactor.interact_one_pair(saucer, missile)
        assert not missiles
        assert not saucers
        return interactor

    def test_small_saucer_ship_missile_scores(self):
        pos = Vector2(100, 100)
        saucer = Saucer(pos, 1)
        interactor = self.destroy_each_other(pos, saucer)
        assert interactor.score == 1000

    def test_saucer_vs_saucer_missile_does_not_score(self):
        pos = Vector2(100, 100)
        saucer = Saucer()
        saucer.move_to(pos)
        saucers = [saucer]
        missile = Missile.from_saucer(pos, Vector2(0, 0))
        missiles = [missile]
        interactor = Interactor(Fleets([], missiles, saucers, [], []))
        interactor.interact_one_pair(saucer, missile)
        assert not missiles
        assert not saucers
        assert interactor.score == 0

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
        interactor = Interactor(Fleets([], [], [], [], []))
        score = interactor.perform_interactions()
        assert score == 0

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
        game.fleets.asteroids.append(asteroid)
        missile = Missile.from_ship(Vector2(100, 100), Vector2(3, 3))
        game.fleets.missiles.append(missile)
        game.process_interactions()
        assert game.score == 20

    def test_cached_collider_is_safe(self):
        asteroid = Asteroid(2, Vector2(100, 100))
        missile = Missile.from_ship(Vector2(100, 100), Vector2(3, 3))
        asteroids = [asteroid]
        missiles = [missile]
        interactor = Interactor(Fleets(asteroids, missiles, [], [], []))
        interactor.perform_interactions()
        assert interactor.score == 20
        interactor.perform_interactions()
        assert interactor.score == 20

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
