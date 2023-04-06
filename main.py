# Example file showing a circle moving on screen
from pygame import Vector2

from asteroid import Asteroid
import pygame
from ship import Ship
import u

ship = Ship(pygame.Vector2(u.SCREEN_SIZE / 2, u.SCREEN_SIZE / 2))
ships = []
asteroids = []
missiles = []
ship_timer = 0
running = False
delta_time = 0
clock = pygame.time.Clock()
asteroids_in_this_wave = 2
wave_timer = None


def game_init():
    global screen, clock, running, delta_time, asteroids_in_this_wave
    global wave_timer, ships
    pygame.init()
    screen = pygame.display.set_mode((u.SCREEN_SIZE, u.SCREEN_SIZE))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    asteroids_in_this_wave = 2
    wave_timer = u.ASTEROID_TIMER_STOPPED
    ships = []
    set_ship_timer(u.SHIP_EMERGENCE_TIME)
    running = True
    delta_time = 0


def main_loop():
    global running, ship, clock, delta_time
    game_init()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        check_ship_spawn(ship, ships, delta_time)
        check_next_wave(asteroids, delta_time)
        control_ship(ship, delta_time)

        for missile in missiles.copy():
            missile.update(missiles, delta_time)

        move_everything(ship, delta_time)
        check_collisions()
        draw_everything()
        pygame.display.flip()
        delta_time = clock.tick(60) / 1000
    pygame.quit()


def check_asteroids_vs_missiles():
    for asteroid in asteroids.copy():
        for missile in missiles.copy():
            asteroid.collide_with_attacker(missile, missiles, asteroids)


def check_asteroids_vs_ship():
    for ship in ships.copy():  # there's only one, do it first
        for asteroid in asteroids.copy():
            asteroid.collide_with_attacker(ship, ships, asteroids)
            if not ships:
                set_ship_timer(u.SHIP_EMERGENCE_TIME)
                return


def check_collisions():
    check_asteroids_vs_ship()
    check_asteroids_vs_missiles()


def check_next_wave(asteroids, dt):
    global wave_timer
    if not asteroids:
        if wave_timer == u.ASTEROID_TIMER_STOPPED:
            wave_timer = u.ASTEROID_DELAY
        else:
            create_wave_in_due_time(asteroids, dt)


def check_ship_spawn(ship, ships, delta_time):
    if ships: return
    global ship_timer
    ship_timer -= delta_time
    if ship_timer <= 0 and safe_to_emerge(missiles, asteroids):
        ship.reset()
        ships.append(ship)


def control_ship(ship, dt):
    keys = pygame.key.get_pressed()
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
    global ship
    screen.fill("midnightblue")
    for ship in ships:
        ship.draw(screen)
    for asteroid in asteroids:
        asteroid.draw(screen)
    for missile in missiles:
        missile.draw(screen)


def move_everything(ship, dt):
    if ship.active: ship.move(dt)
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
    ship_timer = seconds


if __name__ == "__main__":
    main_loop()
