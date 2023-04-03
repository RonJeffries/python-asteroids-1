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
asteroids = [Asteroid(2) for i in range(0, 4)]
missiles = []


def check_collisions():
    if ship.active:
        for asteroid in asteroids.copy():
            ship.collideWithAsteroid(asteroid)
            if not ship.active:
                asteroids.remove(asteroid)
                radius = asteroid.radius
                size = [16, 32, 64].index(radius)
                if size > 0:
                    a1 = Asteroid(size - 1, asteroid.mover.position)
                    asteroids.append(a1)
                    a2 = Asteroid(size - 1, asteroid.mover.position)
                    asteroids.append(a2)
                ship.active = True


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("midnightblue")

    # pygame.draw.circle(screen,"red",(u.SCREEN_SIZE/2, u.SCREEN_SIZE/2), 3)
    if ship.active: ship.draw(screen)
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

    if ship.active: ship.mover.move(dt)
    for asteroid in asteroids:
        asteroid.mover.move(dt)
    for missile in missiles.copy():
        missile.update(missiles, dt)
    for missile in missiles:
        missile.mover.move(dt)
    check_collisions()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
