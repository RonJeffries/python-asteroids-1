import pygame
from pygame import Vector2
from dataclasses import dataclass

import u
from flyer import Flyer
from score import Score
from ship import Ship


@dataclass
class NoShips:
    ships_remaining: int = 0

    def add_ship(self):
        pass


class ScoreKeeper(Flyer):

    available_ship = Ship(Vector2(0, 0))
    available_ship._angle = 90

    @classmethod
    def should_interact_with(cls):
        from score import Score
        return [Score]

    def __init__(self):
        self.score = 0
        self._fence = u.FREE_SHIP_SCORE
        self._ship_maker = NoShips()
        if pygame.get_init():
            self.score_font = pygame.font.SysFont("arial", 48)

    @staticmethod
    def are_we_colliding(_position, _radius):
        return False

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_fragment(self, fragment, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass

    def draw(self, screen):
        score_surface, score_rect = self.render_score()
        screen.blit(score_surface, score_rect)
        self.draw_available_ships(screen)

    def draw_available_ships(self, screen):
        for i in range(0, self._ship_maker.ships_remaining):
            self.draw_available_ship(self.available_ship, i, screen)

    def draw_available_ship(self, ship, i, screen):
        position = i * Vector2(35, 0)
        ship.move_to(Vector2(55, 100) + position)
        ship.draw(screen)

    def render_score(self):
        score_text = f"0000{self.score}"[-5:]
        score_surface = self.score_font.render(score_text, True, "green")
        score_rect = score_surface.get_rect(topleft=(10, 10))
        return score_surface, score_rect

    def interact_with(self, other, fleets):
        other.interact_with_scorekeeper(self, fleets)

    def interact_with_shipmaker(self, shipmaker, fleets):
        self._ship_maker = shipmaker

    def interact_with_score(self, score, fleets):
        self.score += score.score
        if self.score >= self._fence:
            self._ship_maker.add_ship()
            self._fence += u.FREE_SHIP_SCORE

    def tick(self, delta_time, fleets):
        pass
