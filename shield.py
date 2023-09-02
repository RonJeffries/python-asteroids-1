import pygame
from pygame import Mask, Surface, Vector2

from Collider import Collider
from bitmap_maker import BitmapMaker
from flyer import InvadersFlyer
from tasks import Tasks


class Shield(InvadersFlyer):
    def __init__(self, position):
        map = BitmapMaker.instance().shield
        self._invader_shot_explosion = BitmapMaker.instance().invader_shot_explosion
        self._invader_explosion_mask = pygame.mask.from_surface(self._invader_shot_explosion)
        self._player_shot_explosion = BitmapMaker.instance().player_shot_explosion
        self._player_explosion_mask = pygame.mask.from_surface(self._player_shot_explosion)
        self._map = map.copy()
        self._map.set_colorkey("black")
        self._mask = pygame.mask.from_surface(map)
        self._rect = self._map.get_rect()
        self._rect.center = position
        self._tasks = Tasks()

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

    def begin_interactions(self, fleets):
        self._tasks.clear()

    def end_interactions(self, fleets):
        self._tasks.finish()

    def interact_with(self, other, fleets):
        other.interact_with_shield(self, fleets)

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderfleet(self, fleet, fleets):
        pass

    def interact_with_invaderplayer(self, player, fleets):
        pass

    def interact_with_invadershot(self, shot, fleets):
        self.process_shot_collision(shot, self._invader_shot_explosion, self._invader_explosion_mask)

    def interact_with_playerexplosion(self, explosion, fleets):
        pass

    def interact_with_playershot(self, shot, fleets):
        self.process_shot_collision(shot, self._player_shot_explosion, self._player_explosion_mask)

    def process_shot_collision(self, shot, explosion, explosion_mask):
        collider = Collider(self, shot)
        if collider.colliding():
            overlap_mask: Mask = collider.overlap_mask()
            self.update_mask_and_visible_pixels(collider, explosion, explosion_mask, overlap_mask, shot)

    def update_mask_and_visible_pixels(self, collider, explosion, explosion_mask, overlap_mask, shot):
        self._tasks.remind_me(lambda: self.erase_shot_and_explosion_from_mask(shot, collider.offset(), overlap_mask, explosion, explosion_mask))
        self._tasks.remind_me(lambda: self.erase_visible_pixels(overlap_mask, self._mask))

    def erase_shot_and_explosion_from_mask(self, shot, collider_offset, shot_overlap_mask, explosion, explosion_mask):
        self._mask.erase(shot_overlap_mask, (0, 0))
        self.erase_explosion_from_mask(collider_offset, explosion, explosion_mask, shot)

    def erase_explosion_from_mask(self, collider_offset, explosion, explosion_mask, shot):
        # explosion_rect = explosion.get_rect()
        # explosion_rect.center = shot.rect.center
        # adjust_image_to_center = Vector2(explosion_rect.topleft) - Vector2(shot.rect.topleft)
        # print(explosion_rect, shot.rect, adjust_image_to_center)
        expl_rect = explosion_mask.get_rect()
        offset_x = (shot.rect.w - expl_rect.w) // 2
        adjust_image_to_center = collider_offset + Vector2(offset_x, 0)
        self._mask.erase(explosion_mask, adjust_image_to_center)

    def erase_visible_pixels(self, shot_mask, shield_mask):
        rect = shot_mask.get_rect()
        surf = shield_mask.to_surface()
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

