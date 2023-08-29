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
        self.process_shot_collision(shot, self._explosion_mask)

    def interact_with_playerexplosion(self, explosion, fleets):
        pass

    def interact_with_playershot(self, shot, fleets):
        self.process_shot_collision(shot, self._player_explosion_mask)

    def process_shot_collision(self, shot, explosion_mask):
        collider = Collider(self, shot)
        if collider.colliding():
            overlap_mask: Mask = collider.overlap_mask()
            self.erase_shot_and_explosion_from_mask(shot, collider, overlap_mask, explosion_mask)
            self.erase_visible_pixels(overlap_mask)

    def erase_shot_and_explosion_from_mask(self, shot, collider, shot_overlap_mask, explosion_mask):
        self._mask_copy.erase(shot_overlap_mask, (0, 0))
        self.erase_explosion_from_mask(collider, explosion_mask, shot)

    def erase_explosion_from_mask(self, collider, explosion_mask, shot):
        expl_rect = explosion_mask.get_rect()
        offset_x = (shot.rect.w - expl_rect.w) // 2
        adjust_image_to_center = collider.offset() + Vector2(offset_x, 0)
        self._mask_copy.erase(explosion_mask, adjust_image_to_center)

    def erase_visible_pixels(self, shot_mask):
        rect = shot_mask.get_rect()
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

