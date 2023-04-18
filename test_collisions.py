from pygame import Vector2

import main
import u
from asteroid import Asteroid
from game import safe_to_emerge
from missile import Missile
from ship import Ship
from game import Game
import game


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

    def test_safe_to_emerge_hates_missiles(self):
        missiles = []
        asteroids = []
        assert safe_to_emerge(missiles, asteroids)
        missiles.append(Missile(Vector2(0, 0), Vector2(0, 0)))
        assert not safe_to_emerge(missiles, asteroids)

    def test_safe_to_emerge_hates_close_asteroids(self):
        asteroids = []
        missiles = []
        assert safe_to_emerge(missiles, asteroids)
        asteroids.append(Asteroid(2, u.CENTER))
        assert not safe_to_emerge(missiles, asteroids)

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
        u.score = 0
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        asteroids = [asteroid]
        missile = Missile(pos, Vector2(0, 0))
        missiles = [missile]
        game.mutual_destruction(asteroid, asteroids, missile, missiles)
        assert not missiles
        assert u.score == 20
        assert len(asteroids) == 2

    def test_missile_ship_does_not_score(self):
        u.score = 0
        pos = Vector2(100, 100)
        ship = Ship(pos)
        ships = [ship]
        missile = Missile(pos, Vector2(0, 0))
        missiles = [missile]
        game.mutual_destruction(ship, ships, missile, missiles)
        assert not missiles
        assert not ships
        assert u.score == 0

    def test_asteroid_ship_does_not_score(self):
        u.score = 0
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        print("position", asteroid.position)
        asteroids = [asteroid]
        ship = Ship(pos)
        ships = [ship]
        game.mutual_destruction(asteroid, asteroids, ship, ships)
        assert not ships
        assert u.score == 0

    def test_asteroid_saucer_does_not_score(self):
        u.score = 0
        pos = Vector2(100, 100)
        asteroid = Asteroid(2, pos)
        print("position", asteroid.position)
        asteroids = [asteroid]
        saucer = Saucer(pos)
        saucers = [saucer]
        game.mutual_destruction(asteroid, asteroids, saucer, saucers)
        assert not saucers
        assert u.score == 0

    def test_create_asteroid_at_zero(self):
        asteroid = Asteroid(2, Vector2(0, 0))
        assert asteroid.position == Vector2(0, 0)


class Saucer:
    def __init__(self, position=None):
        if position is not None: self.position = position
        self.score_list = [0, 0, 0]
        self.radius = 20

    def destroyed_by(self, attacker, saucers):
        if self in saucers: saucers.remove(self)
