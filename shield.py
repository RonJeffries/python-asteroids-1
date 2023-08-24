import pygame

from bitmap_maker import BitmapMaker
from flyer import InvadersFlyer


class Shield(InvadersFlyer):
    def __init__(self, position):
        maker = BitmapMaker.instance()
        self.map = maker.shield.copy()
        self._mask = pygame.mask.from_surface(self.map)
        self._rect = self.map.get_rect()
        self._rect.center = position

    @property
    def mask(self):
        return self._mask

    @property
    def rect(self):
        return self._rect

    def draw(self, screen):
        screen.blit(self.map, self.rect)

    def interact_with(self, other, fleets):
        other.interact_with_shield(self, fleets)

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

    def tick(self, delta_time, fleets):
        pass

