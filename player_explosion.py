
import pygame
import random

from pygame import Vector2

from bitmap_maker import BitmapMaker
from flyer import InvadersFlyer


class PlayerExplosion(InvadersFlyer):
    def __init__(self, position):
        maker = BitmapMaker.instance()
        self.players = maker.players  # one turret, two explosions
        self.player = self.players[1]
        self._mask = pygame.mask.from_surface(self.player)
        self._rect = self.player.get_rect()
        self._rect.center = position
        self._explode_time = 1

    @property
    def mask(self):
        return self._mask

    @property
    def rect(self):
        return self._rect

    @property
    def position(self):
        return Vector2(self.rect.center)

    def interact_with(self, other, fleets):
        pass

    def draw(self, screen):
        player = self.players[random.randint(1,2)]
        screen.blit(player, self.rect)

    def tick(self, delta_time, fleets):
        self._explode_time -= delta_time
        if self._explode_time <= 0:
            fleets.remove(self)

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderfleet(self, fleet, fleets):
        pass

    def interact_with_invaderplayer(self, player, fleets):
        pass

    def interact_with_invadershot(self, shot, fleets):
        pass

    def interact_with_playerexplosion(self, explosion, fleets):
        pass

    def interact_with_playershot(self, shot, fleets):
        pass

    def interact_with_invaderexplosion(self, explosion, fleets):
        pass

    def interact_with_shield(self, shield, fleets):
        pass

    def interact_with_shotcontroller(self, controller, fleets):
        pass

    def interact_with_shotexplosion(self, bumper, fleets):
        pass

    def interact_with_topbumper(self, top_bumper, fleets):
        pass