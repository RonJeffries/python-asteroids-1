import pygame
from pygame import Mask, Surface

from Collider import Collider
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
        collider = Collider(self, shot)
        if collider.colliding():
            mask: Mask = collider.overlap_mask()
            rect = mask.get_rect()
            map = self.map
            for x in range(rect.right):
                for y in range(rect.bottom):
                    bit = mask.get_at((x, y))
                    if bit:
                        map.set_at((x, y), "black")
                    else:
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

