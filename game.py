# Game

from pygame import Surface, Vector2

from asteroid import Asteroid
import pygame
from ship import Ship
import u

ship = Ship(pygame.Vector2(u.SCREEN_SIZE / 2, u.SCREEN_SIZE / 2))
ships = []


def check_collisions():
    check_individual_collisions(ships, current_instance.asteroids)
    check_individual_collisions(current_instance.asteroids, current_instance.missiles)
    check_individual_collisions(ships, current_instance.missiles)
    if not ships:
        current_instance.set_ship_timer(u.SHIP_EMERGENCE_TIME)


def check_individual_collisions(targets, attackers):
    for target in targets.copy():
        for attacker in attackers.copy():
            if mutual_destruction(target, targets, attacker, attackers):
                break


def mutual_destruction(target, targets, attacker, attackers):
    if within_range(target, attacker):
        attacker.destroyed_by(target, attackers)
        target.destroyed_by(attacker, targets)


def within_range(target, attacker):
    in_range = target.radius + attacker.radius
    dist = target.position.distance_to(attacker.position)
    return dist <= in_range


def check_next_wave(dt):
    if not current_instance.asteroids:
        if current_instance.wave_timer == u.ASTEROID_TIMER_STOPPED:
            current_instance.wave_timer = u.ASTEROID_DELAY
        else:
            create_wave_in_due_time(current_instance.asteroids, dt)


def control_ship(ship, dt):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        current_instance.insert_quarter(u.SHIPS_PER_QUARTER)
    if keys[pygame.K_f]:
        ship.turn_left(dt)
    if keys[pygame.K_d]:
        ship.turn_right(dt)
    if keys[pygame.K_j]:
        ship.power_on(dt)
    else:
        ship.power_off()
    if keys[pygame.K_k]:
        ship.fire_if_possible(current_instance.missiles)
    else:
        ship.not_firing()


def create_wave_in_due_time(asteroids, dt):
    current_instance.wave_timer -= dt
    if current_instance.wave_timer <= 0:
        asteroids.extend([Asteroid() for _ in range(0, next_wave_size())])
        wave_timer = u.ASTEROID_TIMER_STOPPED


def draw_everything():
    screen = current_instance.screen
    screen.fill("midnightblue")
    for ship in ships:
        ship.draw(screen)
    for asteroid in current_instance.asteroids:
        asteroid.draw(screen)
    for missile in current_instance.missiles:
        missile.draw(screen)
    draw_score()
    draw_available_ships()


def draw_available_ships():
    ship = Ship(Vector2(20, 100))
    ship.angle = 90
    for i in range(0, current_instance.ships_remaining):
        draw_available_ship(i, ship)


def draw_available_ship(ship_number, ship):
    ship.position += Vector2(35, 0)
    ship.draw(current_instance.screen)


def draw_game_over():
    screen = current_instance.screen
    screen.blit(current_instance.game_over_surface, current_instance.game_over_pos)
    for text, pos in current_instance.help_lines:
        screen.blit(text, pos)


def draw_score():
    score_surface, score_rect = render_score()
    current_instance.screen.blit(score_surface, score_rect)


def render_score():
    score_text = f"0000{u.score}"[-5:]
    score_surface = current_instance.score_font.render(score_text, True, "green")
    score_rect = score_surface.get_rect(topleft=(10,10))
    return score_surface, score_rect


def next_wave_size():
    current_instance.asteroids_in_this_wave += 2
    if current_instance.asteroids_in_this_wave > 10:
        current_instance.asteroids_in_this_wave = 11
    return current_instance.asteroids_in_this_wave


def safe_to_emerge(missiles, asteroids):
    if missiles: return False
    for asteroid in asteroids:
        if asteroid.position.distance_to(u.CENTER) < u.SAFE_EMERGENCE_DISTANCE:
            return False
    return True




class Game:
    def __init__(self, testing=False):
        self.missiles = []
        self.asteroids = []
        self.asteroids_in_this_wave = None
        self.wave_timer = u.ASTEROID_TIMER_STOPPED
        self.help_lines = None
        self.game_over_pos = None
        self.game_over_surface = None
        self.ship_timer = 0
        self.game_over = False
        self.score_font = None
        self.running = False
        self.delta_time = 0
        self.ships_remaining = 0
        if not testing:
            self.screen = pygame.display.set_mode((u.SCREEN_SIZE, u.SCREEN_SIZE))
            self.clock = pygame.time.Clock()

    def check_ship_spawn(self, ship, ships, delta_time):
        if ships: return
        if self.ships_remaining <= 0:
            self.game_over = True
            return
        self.ship_timer -= delta_time
        if self.ship_timer <= 0 and safe_to_emerge(self.missiles, self.asteroids):
            ship.reset()
            ships.append(ship)
            self.ships_remaining -= 1

    def define_game_over(self):
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

    def define_score(self):
        u.score = 0
        # move to Game class
        self.score_font = pygame.font.SysFont("arial", 48)

    def game_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((u.SCREEN_SIZE, u.SCREEN_SIZE))
        pygame.display.set_caption("Asteroids")
        self.define_game_over()
        self.define_score()
        self.running = True
        self.insert_quarter(0)

    def insert_quarter(self, number_of_ships):
        global missiles, ships
        self.asteroids = []
        self.missiles = []
        ships = []
        self.asteroids_in_this_wave = 2
        self.game_over = False
        u.score = 0
        self.ships_remaining = number_of_ships
        self.set_ship_timer(u.SHIP_EMERGENCE_TIME)
        self.wave_timer = u.ASTEROID_TIMER_STOPPED
        self.delta_time = 0

    def main_loop(self):
        print("In game's loop")
        global game_over_pos
        self.game_init()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.check_ship_spawn(ship, ships, self.delta_time)
            check_next_wave(self.delta_time)
            control_ship(ship, self.delta_time)

            for missile in self.missiles.copy():
                missile.update(self.missiles, self.delta_time)

            self.move_everything(self.delta_time)
            check_collisions()
            draw_everything()
            if self.game_over: draw_game_over()
            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1000
        pygame.quit()

    def move_everything(self,dt):
        for the_ship in ships:
            the_ship.move(dt)
        for asteroid in self.asteroids:
            asteroid.move(dt)
        for missile in self.missiles:
            missile.move(dt)

    def set_instance(self, a_game):
        global current_instance
        current_instance = a_game

    def set_ship_timer(self, seconds):
        if self.ship_timer <= 0:
            self.ship_timer = seconds
