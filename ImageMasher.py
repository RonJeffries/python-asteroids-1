from pygame import Vector2


class ImageMasher:
    def __init__(self, target, shot):
        self.target = target
        self.shot = shot
        self.new_mask = self.target.mask.copy()

    def apply_explosion(self):
        offset = self.shot_offset()
        mask = self.shot.explosion_mask
        self.new_mask.erase(mask, offset)

    def apply_shot(self):
        offset = self.shot_offset()
        overlap = self.target.mask.overlap_mask(self.shot.mask, offset)
        self.new_mask.erase(overlap, (0, 0))

    def get_mask(self):
        return self.new_mask

    def shot_offset(self):
        return Vector2(self.shot.rect.topleft) - Vector2(self.target.rect.topleft)
