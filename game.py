# Game

from fleets import Fleets
from game_over import GameOver
from interactor import Interactor
from pygame import Vector2
from coin import Coin
from ship import Ship
from sounds import player
import pygame
import u


class Game:

    available_ship = Ship(Vector2(0, 0))
    available_ship._angle = 90

    def __init__(self, testing=False):
        self.delta_time = 0
        self.init_pygame_and_display(testing)
        self.fleets = Fleets()
        self.fleets.add_flyer(Coin.slug())

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
            self.fleets.add_flyer(Coin.quarter())

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

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.asteroids_tick(self.delta_time)

            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1000
        pygame.quit()

    def asteroids_tick(self, delta_time):
        self.control_game()
        self.fleets.move(delta_time)
        self.perform_interactions()
        self.fleets.tick(delta_time)
        self.draw_everything()

