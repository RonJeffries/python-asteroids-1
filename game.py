# Game

from pygame import Vector2

import pygame

from interactor import Interactor
from fleet import ShipFleet
from ship import Ship
import u
from fleets import Fleets
from sounds import player


class Game:

    available_ship = Ship(Vector2(0, 0))
    available_ship._angle = 90

    def __init__(self, testing=False):
        self.delta_time = 0
        self.score = 0
        self.fleets = Fleets()
        self.init_pygame_and_display(testing)
        self.running = not testing

    # noinspection PyAttributeOutsideInit
    def init_pygame_and_display(self, testing):
        if testing: return
        pygame.init()
        pygame.mixer.init()
        player.init_sounds()
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((u.SCREEN_SIZE, u.SCREEN_SIZE))
        self.init_game_over()
        self.init_score()

    # noinspection PyAttributeOutsideInit
    def init_game_over(self):
        big_font = pygame.font.SysFont("arial", 64)
        small_font = pygame.font.SysFont("arial", 48)
        self.game_over_surface = big_font.render("GAME OVER", True, "white")
        self.game_over_pos = self.game_over_surface.get_rect(centerx=u.CENTER.x, centery=u.CENTER.y / 2)
        pos_left = u.CENTER.x - 150
        pos_top = self.game_over_pos.centery
        self.help_lines = []
        messages = ["d - turn left", "f - turn right", "j - accelerate", "k - fire missile", "q - insert quarter", ]
        for message in messages:
            pos_top += 60
            text = small_font.render(message, True, "white")
            text_rect = text.get_rect(topleft=(pos_left, pos_top))
            pair = (text, text_rect)
            self.help_lines.append(pair)

    # noinspection PyAttributeOutsideInit
    def init_score(self):
        self.score = 0
        self.score_font = pygame.font.SysFont("arial", 48)

    def process_collisions(self):
        collider = Interactor(self.fleets)
        self.score += collider.perform_interactions()

    def control_game(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            # noinspection PyAttributeOutsideInit
            self.keep_going = True
            self.running = False

    def draw_everything(self):
        screen = self.screen
        screen.fill("midnightblue")
        self.fleets.draw(screen)
        self.draw_score()
        self.draw_available_ships()

    def draw_available_ships(self):
        for i in range(0, ShipFleet.ships_remaining):
            self.draw_available_ship(self.available_ship, i)

    def draw_available_ship(self, ship, i):
        position = i*Vector2(35, 0)
        ship.move_to(Vector2(55, 100) + position)
        ship.draw(self.screen)

    def draw_game_over(self):
        screen = self.screen
        screen.blit(self.game_over_surface, self.game_over_pos)
        for text, pos in self.help_lines:
            screen.blit(text, pos)

    def draw_score(self):
        score_surface, score_rect = self.render_score()
        self.screen.blit(score_surface, score_rect)

    def render_score(self):
        score_text = f"0000{self.score}"[-5:]
        score_surface = self.score_font.render(score_text, True, "green")
        score_rect = score_surface.get_rect(topleft=(10, 10))
        return score_surface, score_rect

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
        self.fleets.tick(delta_time)
        self.control_game()
        self.process_collisions()
        self.draw_everything()
        if ShipFleet.game_over: self.draw_game_over()

