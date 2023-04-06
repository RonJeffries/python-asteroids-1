# Example file showing a circle moving on screen
from pygame import Vector2

from asteroid import Asteroid
import pygame
from ship import Ship
import u

ship = Ship(pygame.Vector2(u.SCREEN_SIZE / 2, u.SCREEN_SIZE / 2))
ships = [ship]
asteroids = []
missiles = []
ship_timer = 0
running = False
dt = 0
clock = pygame.time.Clock()
asteroids_in_this_wave = 2
wave_timer = None


# pygame setup
def game_init():
    global screen, clock, running, dt, asteroids_in_this_wave
    global wave_timer
    pygame.init()
    screen = pygame.display.set_mode((u.SCREEN_SIZE, u.SCREEN_SIZE))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    asteroids_in_this_wave = 2
    wave_timer = None
    running = True
    dt = 0


def set_ship_timer(seconds):
    global ship_timer
    ship_timer = seconds


def check_ship_spawn(ship, ships, delta_time):
    if ships: return
    global ship_timer
    ship_timer -= delta_time
    if ship_timer <= 0 and safe_to_emerge(missiles, asteroids):
        ship.reset()
        ships.append(ship)


def check_asteroids_vs_missiles():
    for asteroid in asteroids.copy():
        for missile in missiles.copy():
            asteroid.collide_with_attacker(missile, missiles, asteroids)


def check_collisions():
    check_asteroids_vs_ship()
    check_asteroids_vs_missiles()


def check_asteroids_vs_ship():
    for ship in ships.copy():  # there's only one, do it first
        for asteroid in asteroids.copy():
            asteroid.collide_with_attacker(ship, ships, asteroids)
            if not ships:
                set_ship_timer(u.SHIP_EMERGENCE_TIME)
                return


def check_next_wave(asteroids, dt):
    global wave_timer
    if asteroids: return
    if not wave_timer:
        wave_timer = u.ASTEROID_DELAY
    else:
        wave_timer -= dt
        if wave_timer <= 0:
            asteroids.extend([Asteroid() for _ in range(0, next_wave_size())])
            wave_timer = None


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


def main_loop():
    global running, ship, clock, dt
    game_init()
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("midnightblue")

        check_ship_spawn(ship, ships, dt)
        check_next_wave(asteroids, dt)

        # pygame.draw.circle(screen,"red",(u.SCREEN_SIZE/2, u.SCREEN_SIZE/2), 3)
        for ship in ships:
            ship.draw(screen)
        for asteroid in asteroids:
            asteroid.draw(screen)
        for missile in missiles:
            missile.draw(screen)

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

        if ship.active: ship.move(dt)
        for asteroid in asteroids:
            asteroid.move(dt)
        for missile in missiles.copy():
            missile.update(missiles, dt)
        for missile in missiles:
            missile.move(dt)
        check_collisions()

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main_loop()
