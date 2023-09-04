from pygame import Vector2


class ImageMasher:
    def __init__(self, target, shot):
        self.target = target
        self.shot = shot
        self.new_mask = self.target.mask.copy()

    def offset(self, point1, point2):
        return Vector2(point1) - Vector2(point2)

    def apply_explosion(self):
        explosion_mask = self.shot.explosion_mask
        explosion_rect = explosion_mask.get_rect()
        explosion_rect.center = self.shot.position
        explosion_offset = self.offset(explosion_rect.topleft, self.target.rect.topleft)
        self.new_mask.erase(explosion_mask, explosion_offset)

    def apply_shot(self):
        offset = self.shot_offset()
        overlap = self.target.mask.overlap_mask(self.shot.mask, offset)
        self.new_mask.erase(overlap, (0, 0))

    def get_mask(self):
        return self.new_mask

    def shot_offset(self):
        return self.offset(self.shot.rect.topleft, self.target.rect.topleft)
