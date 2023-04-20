from pygame import Vector2

import main
import u
from asteroid import Asteroid
from collider import Collider
from missile import Missile
from saucer import Saucer
from ship import Ship
from game import Game


class TestCollisions:
    def test_respawn_ship(self):
        game = Game(testing=True)
        game.ships_remaining = 3
        ship = Ship(Vector2(0, 0))
        ship.velocity = Vector2(31, 32)
        ship.angle = 90
        ships = []
        game.set_ship_timer(3)
        assert game.ship_timer == 3
        game.check_ship_spawn(ship, ships, 0.1)
        assert not ships
        game.check_ship_spawn(ship, ships, u.SHIP_EMERGENCE_TIME)
        assert ships
        assert ship.position == u.CENTER
        assert ship.velocity == Vector2(0, 0)
        assert ship.angle == 0

    def test_respawn_count(self):
        test_game = Game(testing=True)
        ship = Ship(Vector2(0, 0))
        ships = []
        test_game.ships_remaining = 2
        test_game.check_ship_spawn(ship, ships, 3.1)
        assert test_game.ships_remaining == 1
        assert len(ships) == 1
        ships = []
        test_game.check_ship_spawn(ship, ships, 3.1)
        assert test_game.ships_remaining == 0
        assert len(ships) == 1
        ships = []
        test_game.check_ship_spawn(ship, ships, 3.1)
        assert test_game.game_over
        assert not ships

    def test_spawn_saucer(self):
        game = Game(testing=True)
        saucer = game.saucer
        game.game_init()
        game.check_saucer_spawn(saucer, game.saucers, 0.1)
        assert not game.saucers
        game.check_saucer_spawn(saucer, game.saucers, u.SAUCER_EMERGENCE_TIME)
        assert saucer in game.saucers
        assert game.saucer_timer == u.SAUCER_EMERGENCE_TIME

    def test_safe_to_emerge_hates_missiles(self):
        game = Game(True)
        missiles = []
        asteroids = []
        assert game.safe_to_emerge(missiles, asteroids)
        missiles.append(Missile(Vector2(0, 0), Vector2(0, 0)))
        assert not game.safe_to_emerge(missiles, asteroids)

    def test_safe_to_emerge_hates_close_asteroids(self):
        game = Game(True)
        asteroids = []
        missiles = []
        assert game.safe_to_emerge(missiles, asteroids)
        asteroids.append(Asteroid(2, u.CENTER))
        assert not game.safe_to_emerge(missiles, asteroids)

    def test_firing_limit(self):
        ship = Ship(u.CENTER)
        count = 0
        missiles = []
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
        assert ship.score_list == [0, 0, 0]
        missile = Missile(u.CENTER, Vector2(0, 0))
        assert missile.score_list == [100, 50, 20]
        saucer = Saucer()
        assert saucer.score_list == [0, 0, 0]

    def test_missile_asteroid_scores(self):
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        asteroids = [asteroid]
        missile = Missile(pos, Vector2(0, 0))
        missiles = [missile]
        collider = Collider(asteroids, missiles, [], [])
        collider.mutual_destruction(asteroid, asteroids, missile, missiles)
        assert not missiles
        assert collider.score == 20
        assert len(asteroids) == 2

    def test_missile_ship_does_not_score(self):
        pos = Vector2(100, 100)
        ship = Ship(pos)
        ships = [ship]
        missile = Missile(pos, Vector2(0, 0))
        missiles = [missile]
        collider = Collider([], missiles, [], ships)
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
        collider = Collider(asteroids, [], [], ships)
        collider.mutual_destruction(asteroid, asteroids, ship, ships)
        assert not ships
        assert collider.score == 0

    def test_asteroid_saucer_does_not_score(self):
        game = Game(True)
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        print("position", asteroid.position)
        asteroids = [asteroid]
        saucer = Saucer(pos)
        saucers = [saucer]
        collider = Collider(asteroids, [], saucers, [])
        collider.mutual_destruction(asteroid, asteroids, saucer, saucers)
        assert not saucers
        assert game.score == 0

    def test_create_asteroid_at_zero(self):
        asteroid = Asteroid(2, Vector2(0, 0))
        assert asteroid.position == Vector2(0, 0)

    def test_collider(self):
        game = Game(True)
        collider = Collider(asteroids=[], missiles=[], saucers=[], ships=[])
        score = collider.check_collisions()
        assert score == 0

    def test_collider_via_game_with_score(self):
        game = Game(True)
        asteroid = Asteroid(2, Vector2(100, 100))
        game.asteroids=[asteroid]
        missile = Missile(Vector2(100, 100), Vector2(3, 3))
        game.missiles=[missile]
        game.process_collisions()
        assert game.score == 20

    def test_cached_collider_is_safe(self):
        asteroid = Asteroid(2, Vector2(100, 100))
        missile = Missile(Vector2(100, 100), Vector2(3, 3))
        asteroids=[asteroid]
        missiles=[missile]
        collider = Collider(asteroids, missiles, [], [])
        collider.check_collisions()
        assert collider.score == 20
        collider.check_collisions()
        assert collider.score == 20


