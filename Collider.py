from pygame import Vector2


class Collider:
    def __init__(self, left, right):
        self.left_rect = left.rect
        self.left_mask = left.mask
        self.right_rect = right.rect
        self.right_mask = right.mask

    def colliding(self):
        if self.right_rect and self.right_rect and self.left_mask and self.right_mask:
            return self.rectangles_colliding() and self.masks_colliding()
        else:
            return False

    def rectangles_colliding(self):
        return self.left_rect.colliderect(self.right_rect)

    def masks_colliding(self):
        offset = Vector2(self.right_rect.topleft) - Vector2(self.left_rect.topleft)
        return self.left_mask.overlap(self.right_mask, offset)

    def overlap_mask(self):
        offset = Vector2(self.right_rect.topleft) - Vector2(self.left_rect.topleft)
        return self.left_mask.overlap_mask(self.right_mask, offset)
