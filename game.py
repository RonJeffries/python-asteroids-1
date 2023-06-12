# Game

from coin import Coin
from fleets import Fleets
from interactor import Interactor
from sounds import player
import pygame
import u


class Game:
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
        pygame.mixer.set_num_channels(16)
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
        elif keys[pygame.K_a]:
            self.fleets.add_flyer(Coin.no_asteroids())

    def draw_everything(self):
        screen = self.screen
        screen.fill("midnightblue")
        self.fleets.draw(screen)
        self.draw_score()

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

