from pygame import Vector2


class ImageMasher:
    def __init__(self, target, shot):
        self.target = target
        self.shot = shot
        self.new_mask = self.target.mask.copy()

    def determine_damage(self):
        self.apply_shot()
        self.apply_explosion()

    def apply_shot(self):
        shot_mask = self.shot.mask
        self.apply_mask(shot_mask)

    def apply_mask(self, shot_mask):
        shot_offset = self.mask_offset_from_target(shot_mask)
        self.new_mask.erase(shot_mask, shot_offset)

    def apply_explosion(self):
        explosion_mask = self.shot.explosion_mask
        explosion_offset = self.mask_offset_from_target(explosion_mask)
        self.new_mask.erase(explosion_mask, explosion_offset)

    def mask_offset_from_target(self, mask):
        explosion_rectangle = self.mask_rectangle_in_shot_position(mask)
        return self.damage_offset_from_target(explosion_rectangle)

    def mask_rectangle_in_shot_position(self, mask):
        rectangle_moved_to_shot_position = mask.get_rect()
        rectangle_moved_to_shot_position.center = self.shot.position
        return rectangle_moved_to_shot_position

    def damage_offset_from_target(self, damage_rectangle):
        return self.offset(damage_rectangle.topleft, self.target.rect.topleft)

    @staticmethod
    def offset(point1, point2):
        return Vector2(point1) - Vector2(point2)

    def get_new_mask(self):
        return self.new_mask

    def apply_damage_to_surface(self, surface):
        area_to_blit = self.new_mask.get_rect()
        damaged_surface = self.new_mask.to_surface()
        surface.blit(damaged_surface, area_to_blit)
