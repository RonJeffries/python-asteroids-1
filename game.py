# Game

from coin import Coin
from fleets import Fleets
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

    def accept_coins(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.fleets.add_flyer(Coin.quarter())
        elif keys[pygame.K_a]:
            self.fleets.add_flyer(Coin.no_asteroids())

    def prepare_screen(self):
        screen = self.screen
        screen.fill("midnightblue")
        return screen

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.accept_coins()
            self.prepare_screen()
            self.fleets.cycle(self.delta_time, self.screen)

            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1000
        pygame.quit()


