# Example file showing a circle moving on screen
import pygame

from ship import Ship

# pygame setup
pygame.init()
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()
running = True
dt = 0

ship = Ship(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("midnightblue")

    ship.draw(screen)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_f]:
        ship.turn_left(dt)
    if keys[pygame.K_d]:
        ship.turn_right(dt)
    if keys[pygame.K_j]:
        ship.power_on(dt)
    else:
        ship.power_off(dt)
    ship.move(dt)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()