# Game

from pygame import Surface, Vector2

from asteroid import Asteroid
import pygame
from ship import Ship
import u

asteroids = []
asteroids_in_this_wave = 2
clock = pygame.time.Clock()
game_over = False
game_over_surface: Surface
game_over_pos: pygame.rect
missiles = []
running = False
screen: Surface
ship = Ship(pygame.Vector2(u.SCREEN_SIZE / 2, u.SCREEN_SIZE / 2))
ship_timer = 0
ships = []
ships_remaining = u.SHIPS_PER_QUARTER
wave_timer = u.ASTEROID_TIMER_STOPPED


def check_collisions():
    check_individual_collisions(ships, asteroids)
    check_individual_collisions(asteroids, missiles)
    check_individual_collisions(ships, missiles)
    if not ships:
        set_ship_timer(u.SHIP_EMERGENCE_TIME)


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
    global wave_timer
    if not asteroids:
        if wave_timer == u.ASTEROID_TIMER_STOPPED:
            wave_timer = u.ASTEROID_DELAY
        else:
            create_wave_in_due_time(asteroids, dt)


def check_ship_spawn(ship, ships, delta_time):
    global game_over, ship_timer, ships_remaining
    if ships: return
    if ships_remaining <= 0:
        game_over = True
        return
    ship_timer -= delta_time
    if ship_timer <= 0 and safe_to_emerge(missiles, asteroids):
        ship.reset()
        ships.append(ship)
        ships_remaining -= 1


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
        ship.fire_if_possible(missiles)
    else:
        ship.not_firing()


def create_wave_in_due_time(asteroids, dt):
    global wave_timer
    wave_timer -= dt
    if wave_timer <= 0:
        asteroids.extend([Asteroid() for _ in range(0, next_wave_size())])
        wave_timer = u.ASTEROID_TIMER_STOPPED


def draw_everything():
    screen.fill("midnightblue")
    for ship in ships:
        ship.draw(screen)
    for asteroid in asteroids:
        asteroid.draw(screen)
    for missile in missiles:
        missile.draw(screen)
    draw_score()
    draw_available_ships()


def draw_available_ships():
    ship = Ship(Vector2(20, 100))
    ship.angle = 90
    for i in range(0, ships_remaining):
        draw_available_ship(i, ship)


def draw_available_ship(ship_number, ship):
    ship.position += Vector2(35, 0)
    ship.draw(screen)


def draw_game_over():
    screen.blit(game_over_surface, game_over_pos)
    for text, pos in help_lines:
        screen.blit(text, pos)


def draw_score():
    score_surface, score_rect = render_score()
    screen.blit(score_surface, score_rect)


def render_score():
    score_text = f"0000{u.score}"[-5:]
    score_surface = score_font.render(score_text, True, "green")
    score_rect = score_surface.get_rect(topleft=(10,10))
    return score_surface, score_rect


def move_everything(dt):
    for ship in ships:
        ship.move(dt)
    for asteroid in asteroids:
        asteroid.move(dt)
    for missile in missiles:
        missile.move(dt)


def next_wave_size():
    global asteroids_in_this_wave
    asteroids_in_this_wave += 2
    if asteroids_in_this_wave > 10:
        asteroids_in_this_wave = 11
    return asteroids_in_this_wave


def safe_to_emerge(missiles, asteroids):
    if missiles: return False
    for asteroid in asteroids:
        if asteroid.position.distance_to(u.CENTER) < u.SAFE_EMERGENCE_DISTANCE:
            return False
    return True


def set_ship_timer(seconds):
    global ship_timer
    if ship_timer <= 0:
        ship_timer = seconds


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.delta_time = 0

    def set_instance(self, a_game):
        global current_instance
        current_instance = a_game

    def main_loop(self):
        print("In game's loop")
        global running, ship, game_over_surface, game_over_pos
        self.game_init()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            check_ship_spawn(ship, ships, self.delta_time)
            check_next_wave(self.delta_time)
            control_ship(ship, self.delta_time)

            for missile in missiles.copy():
                missile.update(missiles, self.delta_time)

            move_everything(self.delta_time)
            check_collisions()
            draw_everything()
            if game_over: draw_game_over()
            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1000
        pygame.quit()

    def game_init(self):
        global screen, running
        pygame.init()
        screen = pygame.display.set_mode((u.SCREEN_SIZE, u.SCREEN_SIZE))
        pygame.display.set_caption("Asteroids")
        self.define_game_over()
        self.define_score()
        running = True
        self.insert_quarter(0)

    def define_game_over(self):
        global game_over_surface, game_over_pos, help_lines
        big_font = pygame.font.SysFont("arial", 64)
        small_font = pygame.font.SysFont("arial", 48)
        game_over_surface = big_font.render("GAME OVER", True, "white")
        game_over_pos = game_over_surface.get_rect(centerx=u.CENTER.x, centery=u.CENTER.y / 2)
        pos_left = u.CENTER.x - 150
        pos_top = game_over_pos.centery
        help_lines = []
        messages = ["d - turn left", "f - turn right", "j - accelerate", "k - fire missile", "q - insert quarter", ]
        for message in messages:
            pos_top += 60
            text = small_font.render(message, True, "white")
            text_rect = text.get_rect(topleft=(pos_left, pos_top))
            pair = (text, text_rect)
            help_lines.append(pair)

    def define_score(self):
        global score_font
        u.score = 0
        # move to Game class
        score_font = pygame.font.SysFont("arial", 48)

    def insert_quarter(self, number_of_ships):
        global running
        global asteroids, missiles, ships
        global asteroids_in_this_wave, game_over, ships_remaining
        global wave_timer
        asteroids = []
        missiles = []
        ships = []
        asteroids_in_this_wave = 2
        game_over = False
        u.score = 0
        ships_remaining = number_of_ships
        set_ship_timer(u.SHIP_EMERGENCE_TIME)
        wave_timer = u.ASTEROID_TIMER_STOPPED
        self.delta_time = 0
