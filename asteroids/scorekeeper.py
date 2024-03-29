

from asteroids.ship import Ship
from asteroids.shipmaker import ShipMaker
from dataclasses import dataclass
from flyer import AsteroidFlyer
from pygame import Vector2
import pygame
import u


@dataclass
class FakeShipMaker:
    def ships_remaining(self, _ignored):
        return 0

    def add_ship(self):
        pass


class ScoreKeeper(AsteroidFlyer):

    def interact_with_fragment(self, fragment, fleets):
        pass

    def interact_with_gameover(self, game_over, fleets):
        pass

    def interact_with_saucermaker(self, saucermaker, fleets):
        pass

    def interact_with_scorekeeper(self, scorekeeper, fleets):
        pass

    def interact_with_thumper(self, thumper, fleets):
        pass

    def interact_with_wavemaker(self, wavemaker, fleets):
        pass

    available_ship = Ship(Vector2(0, 0), 1)
    available_ship._angle = 90

    @classmethod
    def should_interact_with(cls):
        from asteroids.score import Score
        return [Score]

    def __init__(self, player_number=0):
        self.score = 0
        self._fence = u.FREE_SHIP_SCORE
        self._player_number = player_number
        self._scoring = player_number == 0
        self._ship_maker: ShipMaker | FakeShipMaker = FakeShipMaker()
        if pygame.get_init():
            self.score_font = pygame.font.SysFont("arial", 48)

    @staticmethod
    def are_we_colliding(_position, _radius):
        return False

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass

    def draw(self, screen):
        score_surface, score_destination = self.render_score()
        screen.blit(score_surface, score_destination)
        self.draw_available_ships(screen)

    def draw_available_ships(self, screen):
        count = self._ship_maker.ships_remaining(self._player_number)
        for i in range(0, count):
            self.draw_available_ship(self.available_ship, i, screen)

    def draw_available_ship(self, ship, i, screen):
        x_position = [55, u.SCREEN_SIZE - 55][self._player_number]
        position = i * Vector2(35, 0)
        if self._player_number == 1:
            position = - position
        ship.move_to(Vector2(x_position, 100) + position)
        ship.draw(screen)

    def render_score(self):
        x_position = [10, 875][self._player_number]
        score_text = f"0000{self.score}"[-5:]
        color = "green" if self._scoring else "gray50"
        score_surface = self.score_font.render(score_text, True, color)
        score_destination = (x_position, 10)
        return score_surface, score_destination

    def interact_with(self, other, fleets):
        other.interact_with_scorekeeper(self, fleets)

    def interact_with_shipmaker(self, shipmaker, fleets):
        self._ship_maker = shipmaker

    def interact_with_score(self, score, fleets):
        if self._scoring:
            self.score += score.score
            if self.score >= self._fence:
                self._ship_maker.add_ship(self._player_number)
                self._fence += u.FREE_SHIP_SCORE

    def interact_with_signal(self, signal, fleets):
        self._scoring = signal.signal == self._player_number

    def tick(self, delta_time, fleets):
        pass
