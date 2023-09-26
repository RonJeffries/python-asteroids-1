import pygame

from invaders.Collider import Collider
from invaders.ImageMasher import ImageMasher
from invaders.bitmap_maker import BitmapMaker
from flyer import InvadersFlyer
from core.tasks import Tasks


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

    @property
    def position(self):
        return self._rect.center

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

    def interact_with_invadershot(self, shot, fleets):
        self.process_shot_collision(shot, self._invader_shot_explosion, self._invader_explosion_mask)

    def interact_with_playershot(self, shot, fleets):
        self.process_shot_collision(shot, self._player_shot_explosion, self._player_explosion_mask)

    def process_shot_collision(self, shot, explosion, explosion_mask):
        collider = Collider(self, shot)
        if collider.colliding():
            self._tasks.remind_me(lambda: self.mash_image(shot))
            # overlap_mask: Mask = collider.overlap_mask()
            # self.update_mask_and_visible_pixels(collider, explosion, explosion_mask, overlap_mask, shot)

    def mash_image(self, shot):
        masher = ImageMasher.from_flyers(self, shot)
        masher.determine_damage()
        self._mask = masher.get_new_mask()
        masher.apply_damage_to_surface(self._map)

