from pygame import Vector2


class ImageMasher:
    def __init__(self, target, shot):
        self.target = target
        self.shot = shot
        self.new_mask = self.target.mask.copy()

    def apply_shot(self):
        shot_overlap = self.shot_overlap_mask()
        self.new_mask.erase(shot_overlap, (0, 0))

    def shot_overlap_mask(self):
        return self.target.mask.overlap_mask(self.shot.mask, self.shot_offset())

    def apply_explosion(self):
        explosion_mask = self.shot.explosion_mask
        explosion_offset = self.explosion_offset(explosion_mask)
        self.new_mask.erase(explosion_mask, explosion_offset)

    def explosion_offset(self, explosion_mask):
        explosion_rectangle = self.explosion_rectangle(explosion_mask)
        return self.damage_offset_from_target(explosion_rectangle)

    def explosion_rectangle(self, explosion_mask):
        explosion_rect_moved_to_shot_position = explosion_mask.get_rect()
        explosion_rect_moved_to_shot_position.center = self.shot.position
        return explosion_rect_moved_to_shot_position

    def shot_offset(self):
        return self.damage_offset_from_target(self.shot.rect)

    def damage_offset_from_target(self, damage_rectangle):
        return self.offset(damage_rectangle.topleft, self.target.rect.topleft)

    @staticmethod
    def offset(point1, point2):
        return Vector2(point1) - Vector2(point2)

    def get_new_mask(self):
        return self.new_mask
