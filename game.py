# Game

from pygame import Vector2

from asteroid import Asteroid
import pygame

from collider import Collider
from fleet import ShipFleet
from saucer import Saucer
from ship import Ship
import u
from fleets import Fleets
from timer import Timer


class Game:
    def __init__(self, testing=False):
        self.init_general_game_values()
        self.init_asteroids_game_values()
        self.init_fleets()
        # self.init_timers()
        self.init_pygame_and_display(testing)
        if not testing:
            self.insert_quarter(u.SHIPS_PER_QUARTER)

    # noinspection PyAttributeOutsideInit
    def init_general_game_values(self):
        self.delta_time = 0
        self.game_over = False
        self.running = False
        self.score = 0

    # noinspection PyAttributeOutsideInit
    def init_asteroids_game_values(self):
        self.ships_remaining = 0

    # noinspection PyAttributeOutsideInit
    def init_fleets(self):
        asteroids = []
        missiles = []
        saucers = []
        saucer_missiles = []
        self.ship = Ship(pygame.Vector2(u.SCREEN_SIZE / 2, u.SCREEN_SIZE / 2))
        ships = []
        self.fleets = Fleets(asteroids, missiles, saucers, saucer_missiles, ships)

    @property
    def asteroids(self):
        return self.fleets.asteroids

    @property
    def missiles(self):
        return self.fleets.missiles

    @property
    def saucers(self):
        return self.fleets.saucers

    @property
    def saucer_missiles(self):
        return self.fleets.saucer_missiles

    @property
    def ships(self):
        return self.fleets.ships

    # noinspection PyAttributeOutsideInit
    def init_pygame_and_display(self, testing):
        if testing: return
        pygame.init()
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
        collider = Collider(self.fleets)
        self.score += collider.check_collisions()

    def control_game(self, ship, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.keep_going = True
            self.running = False

    def draw_everything(self):
        screen = self.screen
        screen.fill("midnightblue")
        self.fleets.draw(screen)
        self.draw_score()
        self.draw_available_ships()

    def draw_available_ships(self):
        ship = Ship(Vector2(20, 100))
        ship.angle = 90
        for i in range(0, ShipFleet.ships_remaining):
            self.draw_available_ship(ship)

    def draw_available_ship(self, ship):
        ship.position += Vector2(35, 0)
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
    def game_init(self):
        self.running = True
        Saucer.init_for_new_game()
        self.insert_quarter(u.SHIPS_PER_QUARTER)

    # noinspection PyAttributeOutsideInit
    def insert_quarter(self, number_of_ships):
        self.fleets.clear()
        self.game_over = False
        self.score = 0
        self.ships_remaining = number_of_ships  # TODO remove
        self.delta_time = 0

    def main_loop(self):
        self.game_init()
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
        self.control_game(self.ship, delta_time)
        self.process_collisions()
        self.draw_everything()
        if ShipFleet.game_over: self.draw_game_over()

