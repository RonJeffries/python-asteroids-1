import pygame
from pygame import Mask, Surface, Vector2

from Collider import Collider
from bitmap_maker import BitmapMaker
from flyer import InvadersFlyer


class Shield(InvadersFlyer):
    def __init__(self, position):
        map = BitmapMaker.instance().shield
        explo = BitmapMaker.instance().invader_shot_explosion
        self._explosion_mask = pygame.mask.from_surface(explo)
        player_explo = BitmapMaker.instance().player_shot_explosion
        self._player_explosion_mask = pygame.mask.from_surface(player_explo)
        self._map = map.copy()
        self._map.set_colorkey("black")
        self._mask = pygame.mask.from_surface(map)
        self._mask_copy = self.mask.copy()
        self._rect = self._map.get_rect()
        self._rect.center = position

    @property
    def mask(self):
        return self._mask

    @property
    def rect(self):
        return self._rect

    def draw(self, screen):
        screen.blit(self._map, self.rect)

        # mask_rect = self.rect.copy()
        # mask_rect.centery = self.rect.centery - 96
        # mask_surf = self._mask.to_surface()
        # mask_surf.set_colorkey("black")
        # screen.blit(mask_surf, mask_rect)

    def end_interactions(self, fleets):
        self._mask = self._mask_copy.copy()
        pass

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
            explosion_mask = self._explosion_mask
            self.apply_shield_damage(collider, shot, explosion_mask)

    def interact_with_playerexplosion(self, explosion, fleets):
        pass

    def interact_with_playershot(self, shot, fleets):
        collider = Collider(self, shot)
        if collider.colliding():
            explosion_mask = self._player_explosion_mask
            self.apply_shield_damage(collider, shot, explosion_mask)

    def apply_shield_damage(self, collider, shot, explosion_mask):
        mask: Mask = collider.overlap_mask()
        self._mask_copy.erase(mask, (0, 0))
        rect = mask.get_rect()
        e_rect = explosion_mask.get_rect()
        offset_x = (shot.rect.width - e_rect.width) // 2
        self._mask_copy.erase(explosion_mask, collider.offset() + Vector2(offset_x, 0))
        surf = self._mask_copy.to_surface()
        self._map.blit(surf, rect)

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

