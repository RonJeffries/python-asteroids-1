from pygame import Vector2

from ImageMasher import Masker


class Collider:
    def __init__(self, left, right):
        self.left_masker = Masker(left.mask, left.position)
        self.right_masker = Masker(right.mask, right.position)
        self.left_rect = left.rect
        self.left_mask = left.mask
        self.right_rect = right.rect
        self.right_mask = right.mask

    def colliding(self):
        return self.left_masker.colliding(self.right_masker)

    def rectangles_colliding(self):
        return self.left_rect.colliderect(self.right_rect)

    def masks_colliding(self):
        return self.left_mask.overlap(self.right_mask, self.offset())

    def offset(self):
        offset = Vector2(self.right_rect.topleft) - Vector2(self.left_rect.topleft)
        return offset

    def overlap_mask(self):
        return self.left_mask.overlap_mask(self.right_mask, self.offset())
