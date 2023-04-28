# Game

from pygame import Vector2

from asteroid import Asteroid
import pygame

from collider import Collider
from saucer import Saucer
from ship import Ship
import u
from timer import Timer

class Game:
    def __init__(self, testing=False):
        self.init_general_game_values()
        self.init_asteroids_game_values()
        self.init_space_objects()
        # self.init_timers()
        self.init_pygame_and_display(testing)

    # noinspection PyAttributeOutsideInit
    def init_general_game_values(self):
        self.delta_time = 0
        self.game_over = False
        self.running = False
        self.score = 0

    # noinspection PyAttributeOutsideInit
    def init_asteroids_game_values(self):
        self.asteroids_in_this_wave: int
        self.init_saucer_timer()
        self.set_ship_timer(u.SHIP_EMERGENCE_TIME)
        self.ships_remaining = 0
        self.init_wave_timer()

    def init_saucer_timer(self):
        self.saucer_timer = Timer(u.SAUCER_EMERGENCE_TIME, self.bring_in_saucer)

    # noinspection PyAttributeOutsideInit
    def init_space_objects(self):
        self.asteroids = []
        self.missiles = []
        self.saucer = Saucer(Vector2(u.SCREEN_SIZE / 4, u.SCREEN_SIZE / 4))
        self.saucers = []
        self.saucer_missiles = []
        self.ship = Ship(pygame.Vector2(u.SCREEN_SIZE / 2, u.SCREEN_SIZE / 2))
        self.ships = []

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
        collider = Collider(asteroids=self.asteroids, missiles=self.missiles, saucers=self.saucers, saucer_missiles=self.saucer_missiles,
                            ships=self.ships)
        self.score += collider.check_collisions()

    def check_next_wave(self, delta_time):
        if not self.asteroids:
            self.wave_timer.tick(delta_time, self.asteroids)

    def check_saucer_spawn(self, saucer, saucers, delta_time):
        if saucers: return
        self.saucer_timer.tick(delta_time, saucer, saucers)

    def bring_in_saucer(self, saucer, saucers):
        saucer.ready()
        saucers.append(saucer)

    def check_ship_spawn(self, ship, ships, delta_time):
        if ships: return
        if self.ships_remaining <= 0:
            self.game_over = True
            return
        self.ship_timer.tick(delta_time, ship, ships)

    def spawn_ship_when_ready(self, ship, ships):
        if not self.safe_to_emerge(self.missiles, self.asteroids):
            return False
        ship.reset()
        ships.append(ship)
        self.ships_remaining -= 1
        return True

    def control_ship(self, ship, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.insert_quarter(u.SHIPS_PER_QUARTER)
        if keys[pygame.K_f]:
            ship.turn_left(dt)
        if keys[pygame.K_d]:
            ship.turn_right(dt)
        if keys[pygame.K_j]:
            ship.power_on(dt)
        else:
            ship.power_off()
        if keys[pygame.K_k]:
            ship.fire_if_possible(self.missiles)
        else:
            ship.not_firing()

    def create_wave(self, asteroids):
        asteroids.extend([Asteroid() for _ in range(0, self.next_wave_size())])

    def draw_everything(self):
        screen = self.screen
        screen.fill("midnightblue")
        for saucer in self.saucers:
            saucer.draw(screen)
        for missile in self.saucer_missiles:
            missile.draw(screen)
        for ship in self.ships:
            ship.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw(screen)
        for missile in self.missiles:
            missile.draw(screen)
        self.draw_score()
        self.draw_available_ships()

    def draw_available_ships(self):
        ship = Ship(Vector2(20, 100))
        ship.angle = 90
        for i in range(0, self.ships_remaining):
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

    def game_init(self):
        self.running = True
        self.saucer.init_for_new_game()
        self.insert_quarter(0)

    def insert_quarter(self, number_of_ships):
        self.asteroids = []
        self.missiles = []
        self.ships = []
        self.asteroids_in_this_wave = 2
        self.game_over = False
        self.init_saucer_timer()
        self.score = 0
        self.ships_remaining = number_of_ships
        self.set_ship_timer(u.SHIP_EMERGENCE_TIME)
        self.init_wave_timer()
        self.delta_time = 0

    def init_wave_timer(self):
        self.wave_timer = Timer(u.ASTEROID_DELAY, self.create_wave)

    def main_loop(self):
        self.game_init()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.asteroids_tick(self.delta_time)

            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1000
        pygame.quit()

    def asteroids_tick(self, delta_time):
        self.check_saucer_spawn(self.saucer, self.saucers, delta_time)
        self.check_ship_spawn(self.ship, self.ships, delta_time)
        self.check_next_wave(delta_time)
        self.check_missile_timeout(self.delta_time)
        self.control_ship(self.ship, delta_time)
        self.move_everything(delta_time)
        self.process_collisions()
        self.draw_everything()
        if self.game_over: self.draw_game_over()

    def check_missile_timeout(self, delta_time):
        for missile in self.missiles.copy():
            missile.update(self.missiles, delta_time)
        for missile in self.saucer_missiles.copy():
            missile.update(self.saucer_missiles, delta_time)

    def move_everything(self, delta_time):
        for the_saucer in self.saucers.copy():
            the_saucer.move(delta_time, self.saucers, self.saucer_missiles, self.ships)
        for missile in self.saucer_missiles:
            missile.move(delta_time)
        for the_ship in self.ships:
            the_ship.move(delta_time)
        for asteroid in self.asteroids:
            asteroid.move(delta_time)
        for missile in self.missiles:
            missile.move(delta_time)

    def next_wave_size(self):
        self.asteroids_in_this_wave += 2
        if self.asteroids_in_this_wave > 10:
            self.asteroids_in_this_wave = 11
        return self.asteroids_in_this_wave

    def safe_to_emerge(self, missiles, asteroids):
        if missiles: return False
        for asteroid in asteroids:
            if asteroid.position.distance_to(u.CENTER) < u.SAFE_EMERGENCE_DISTANCE:
                return False
        return True

    def set_ship_timer(self, seconds):
        self.ship_timer = Timer(seconds, self.spawn_ship_when_ready)
