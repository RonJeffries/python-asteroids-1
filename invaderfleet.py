import pygame
from pygame import Vector2

import u
from flyer import Flyer
from invader import Invader


class InvaderFleet(Flyer):
    def __init__(self):
        self.invaders = [Invader(x//5, x % 5) for x in range(55)]
        self.origin = Vector2(u.SCREEN_SIZE / 2 - 5*64, 512)
        self.reverse = False
        self.update(0, None)

    def update(self, delta_time, _fleets):
        for invader in self.invaders:
            invader.move_relative(self.origin)

    def at_edge(self):
        self.reverse = True

    def draw(self, screen):
        pos = u.CENTER
        hw = Vector2(100, 200)
        rect = (pos - hw/2,  hw)
        pygame.draw.rect(screen, "blue", rect)
        step = 64
        for invader in self.invaders:
            invader.draw(screen)

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass

    def interact_with(self, other, fleets):
        pass

    def tick(self, delta_time, fleets):
        pass