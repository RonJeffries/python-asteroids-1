from pygame import Vector2


class ImageMasher:
    @classmethod
    def from_flyers(cls, target, shot):
        return cls(target.mask, target.rect.topleft, shot.mask, shot.position, shot.explosion_mask)

    def __init__(self, target_mask, target_topleft, shot_mask, shot_position, explosion_mask):
        self.target_topleft = target_topleft
        self.shot_mask = shot_mask
        self.shot_position = shot_position
        self.explosion_mask = explosion_mask
        self.new_mask = target_mask.copy()

    def determine_damage(self):
        self.erase_shot()
        self.erase_explosion()

    def erase_shot(self):
        self.erase_mask(self.shot_mask)

    def erase_explosion(self):
        self.erase_mask(self.explosion_mask)

    def erase_mask(self, shot_mask):
        shot_offset = self.mask_offset_from_target(shot_mask)
        self.new_mask.erase(shot_mask, shot_offset)

    def mask_offset_from_target(self, mask):
        explosion_rectangle = self.mask_rectangle_in_shot_position(mask)
        return self.damage_offset_from_target(explosion_rectangle)

    def mask_rectangle_in_shot_position(self, mask):
        rectangle_moved_to_shot_position = mask.get_rect()
        rectangle_moved_to_shot_position.center = self.shot_position
        return rectangle_moved_to_shot_position

    def damage_offset_from_target(self, damage_rectangle):
        return self.offset(damage_rectangle.topleft, self.target_topleft)

    @staticmethod
    def offset(point1, point2):
        return Vector2(point1) - Vector2(point2)

    def get_new_mask(self):
        return self.new_mask

    def apply_damage_to_surface(self, surface):
        area_to_blit = self.new_mask.get_rect()
        damaged_surface = self.new_mask.to_surface()
        surface.blit(damaged_surface, area_to_blit)
