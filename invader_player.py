import pygame

import u
from bitmap_maker import BitmapMaker
from flyer import Flyer


class InvaderPlayer(Flyer):
    def __init__(self):
        maker = BitmapMaker.instance()
        self.players = maker.players  # one turret, two explosions
        self.player = self.players[0]
        self.rect = pygame.Rect(0, 0, 64, 32)
        self.rect.center = (u.SCREEN_SIZE/2, u.SCREEN_SIZE - 5*32 - 16)

    def interact_with(self, other, fleets):
        pass

    def draw(self, screen):
        screen.blit(self.player, self.rect)

    def tick(self, delta_time, fleets):
        pass

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass