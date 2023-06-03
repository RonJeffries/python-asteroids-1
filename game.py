# Game

from pygame import Vector2

import pygame

from game_over import GameOver
from interactor import Interactor
from saucermaker import SaucerMaker
from scorekeeper import ScoreKeeper
from ship import Ship
import u
from fleets import Fleets
from shipmaker import ShipMaker
from sounds import player
from thumper import Thumper
from wavemaker import WaveMaker


class Game:

    available_ship = Ship(Vector2(0, 0))
    available_ship._angle = 90

    def __init__(self, testing=False):
        self.delta_time = 0
        self.init_pygame_and_display(testing)
        self.fleets = Fleets()
        self.fleets.add_flyer(GameOver())
        self.running = not testing

    # noinspection PyAttributeOutsideInit
    def init_pygame_and_display(self, testing):
        if testing:
            return
        pygame.init()
        pygame.mixer.init()
        player.init_sounds()
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((u.SCREEN_SIZE, u.SCREEN_SIZE))

    def perform_interactions(self):
        Interactor(self.fleets).perform_interactions()

    def control_game(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.fleets = Fleets()
            self.fleets.add_flyer(ScoreKeeper(False))
            self.fleets.add_flyer(WaveMaker())
            self.fleets.add_flyer(SaucerMaker())
            self.fleets.add_flyer(ShipMaker())
            self.fleets.add_flyer(Thumper())

    def draw_everything(self):
        screen = self.screen
        screen.fill("midnightblue")
        self.fleets.draw(screen)
        self.draw_score()
        self.draw_available_ships()

    def draw_available_ships(self):
        for i in range(0, self.fleets.ships_remaining):
            self.draw_available_ship(self.available_ship, i)

    def draw_available_ship(self, ship, i):
        position = i*Vector2(35, 0)
        ship.move_to(Vector2(55, 100) + position)
        ship.draw(self.screen)

    def draw_score(self):
        pass

    # noinspection PyAttributeOutsideInit
    def main_loop(self):
        self.keep_going = False
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.keep_going = False

            self.asteroids_tick(self.delta_time)

            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1000
        pygame.quit()
        return self.keep_going

    def asteroids_tick(self, delta_time):
        self.control_game()
        self.fleets.move(delta_time)
        self.perform_interactions()
        self.fleets.tick(delta_time)
        self.draw_everything()

