# Example file showing a circle moving on screen

from asteroid import Asteroid
import pygame
from ship import Ship
import u

# pygame setup
pygame.init()
screen = pygame.display.set_mode((u.SCREEN_SIZE, u.SCREEN_SIZE))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()
running = True
dt = 0

ship = Ship(pygame.Vector2(u.SCREEN_SIZE / 2, u.SCREEN_SIZE / 2))
ships = [ship]
asteroids = [Asteroid(2) for i in range(0, 4)]
missiles = []


def check_asteroids_vs_missiles():
    for asteroid in asteroids.copy():
        for missile in missiles.copy():
            asteroid.collide_with_attacker(missile, missiles, asteroids)


def check_collisions():
    check_ship_vs_asteroid()
    check_asteroids_vs_missiles()


def check_ship_vs_asteroid():
    for ship in ships:
        for asteroid in asteroids.copy():
            asteroid.collide_with_attacker(ship, ships, asteroids)
            if not ships:
                ship.active = True
                ships.append(ship)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("midnightblue")

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
