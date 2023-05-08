from pygame import Vector2

import main
import u
from asteroid import Asteroid
from collider import Collider
from fleet import SaucerFleet, MissileFleet
from missile import Missile
from saucer import Saucer, nearest, nearest_point
from ship import Ship
from game import Game
from fleets import Fleets


class TestCollisions:
    def test_firing_limit(self):
        ship = Ship(u.CENTER)
        count = 0
        missiles = MissileFleet([], u.MISSILE_LIMIT)
        while len(missiles) < u.MISSILE_LIMIT:
            ship.can_fire = True
            ship.fire_if_possible(missiles)
            count += 1
            assert len(missiles) == count
        assert len(missiles) == u.MISSILE_LIMIT
        ship.can_fire = True
        ship.fire_if_possible(missiles)
        assert len(missiles) == u.MISSILE_LIMIT

    # it's barely possible for two missiles to kill the
    # same asteroid. This used to cause a crash, trying
    # to remove the same asteroid twice.
    def test_dual_kills(self):
        asteroid = Asteroid(2, Vector2(0, 0))
        asteroids = [asteroid]
        asteroid.split_or_die(asteroids)
        assert asteroid not in asteroids
        assert len(asteroids) == 2
        asteroid.split_or_die(asteroids)
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
        collider = Collider(Fleets(asteroids, missiles, [], [], []))
        collider.mutual_destruction(asteroid, asteroids, missile, missiles)
        assert not missiles
        assert collider.score == 20
        assert len(asteroids) == 2

    def test_missile_ship_does_not_score(self):
        pos = Vector2(100, 100)
        ship = Ship(pos)
        ships = [ship]
        missile = Missile.from_ship(pos, Vector2(0, 0))
        missiles = [missile]
        collider = Collider(Fleets([], missiles, [], [], ships))
        collider.mutual_destruction(ship, ships, missile, missiles)
        assert not missiles
        assert not ships
        assert collider.score == 0

    def test_asteroid_ship_does_not_score(self):
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        asteroids = [asteroid]
        ship = Ship(pos)
        ships = [ship]
        collider = Collider(Fleets(asteroids, [], [], [], ships))
        collider.mutual_destruction(asteroid, asteroids, ship, ships)
        assert not ships
        assert collider.score == 0

    def test_saucer_ship_does_not_score(self):
        pos = Vector2(100, 100)
        saucer = Saucer()
        saucer.position = pos
        saucers = [saucer]
        ship = Ship(pos)
        ships = [ship]
        collider = Collider(Fleets([], [], saucers, [], ships))
        collider.mutual_destruction(saucer, saucers, ship, ships)
        assert not ships
        assert collider.score == 0

    def test_asteroid_saucer_does_not_score(self):
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        asteroids = [asteroid]
        saucer = Saucer()
        saucer.position = pos
        saucers = [saucer]
        collider = Collider(Fleets(asteroids, [], saucers, [], []))
        collider.mutual_destruction(asteroid, asteroids, saucer, saucers)
        assert not saucers
        assert collider.score == 0

    def test_saucer_ship_missile_scores(self):
        pos = Vector2(100, 100)
        saucer = Saucer()
        saucer.position = pos
        saucers = [saucer]
        missile = Missile.from_ship(pos, Vector2(0, 0))
        missiles = [missile]
        collider = Collider(Fleets([], missiles, saucers, [], []))
        collider.mutual_destruction(saucer, saucers, missile, missiles)
        assert not missiles
        assert not saucers
        assert collider.score == 200

    def test_small_saucer_ship_missile_scores(self):
        pos = Vector2(100, 100)
        saucer = Saucer(pos, 1)
        saucer.position = pos
        saucers = [saucer]
        missile = Missile.from_ship(pos, Vector2(0, 0))
        missiles = [missile]
        collider = Collider(Fleets([], missiles, saucers, [], []))
        collider.mutual_destruction(saucer, saucers, missile, missiles)
        assert not missiles
        assert not saucers
        assert collider.score == 1000

    def test_saucer_vs_saucer_missile_does_not_score(self):
        pos = Vector2(100, 100)
        saucer = Saucer()
        saucer.position = pos
        saucers = [saucer]
        missile = Missile.from_saucer(pos, Vector2(0, 0))
        missiles = [missile]
        collider = Collider(Fleets([], missiles, saucers, [], []))
        collider.mutual_destruction(saucer, saucers, missile, missiles)
        assert not missiles
        assert not saucers
        assert collider.score == 0

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
        game = Game(True)
        collider = Collider(Fleets([], [], [], [], []))
        score = collider.check_collisions()
        assert score == 0

    def test_collider_via_game_with_score(self):
        game = Game(True)
        asteroid = Asteroid(2, Vector2(100, 100))
        game.fleets.asteroids.append(asteroid)
        missile = Missile.from_ship(Vector2(100, 100), Vector2(3, 3))
        game.fleets.missiles.append(missile)
        game.process_collisions()
        assert game.score == 20

    def test_cached_collider_is_safe(self):
        asteroid = Asteroid(2, Vector2(100, 100))
        missile = Missile.from_ship(Vector2(100, 100), Vector2(3, 3))
        asteroids=[asteroid]
        missiles=[missile]
        collider = Collider(Fleets(asteroids, missiles, [], [], []))
        collider.check_collisions()
        assert collider.score == 20
        collider.check_collisions()
        assert collider.score == 20

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



