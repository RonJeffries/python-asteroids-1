from pygame import Vector2


class ImageMasher:
    def __init__(self, target, shot):
        self.target = target
        self.shot = shot
        print("masher center", target.rect.center, shot.rect.center, self.diff(target.rect.center, shot.rect.center))
        print("masher top", target.rect.topleft, shot.rect.topleft, self.diff(target.rect.topleft, shot.rect.topleft))
        self.new_mask = self.target.mask.copy()

    def diff(self, rect1, rect2):
        return Vector2(rect2) - Vector2(rect1)

    def apply_explosion(self):
        offset = self.shot_offset()
        print("masher offset", offset)
        mask = self.shot.explosion_mask
        rect = mask.get_rect()
        center = Vector2(rect.center)
        center = Vector2(0, 0)
        self.new_mask.erase(mask, offset - center)

    def apply_shot(self):
        offset = self.shot_offset()
        overlap = self.target.mask.overlap_mask(self.shot.mask, offset)
        self.new_mask.erase(overlap, (0, 0))

    def get_mask(self):
        return self.new_mask

    def shot_offset(self):
        return Vector2(self.shot.rect.topleft) - Vector2(self.target.rect.topleft)
