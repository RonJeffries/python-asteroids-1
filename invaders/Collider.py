from pygame import Vector2

from invaders.ImageMasher import Masker


class Collider:
    def __init__(self, left, right):
        try:
            self.left_masker = left._sprite
            self.right_masker = right._sprite
        except AttributeError:
            self.left_masker = Masker(left.mask, left.position)
            self.right_masker = Masker(right.mask, right.position)

    def colliding(self):
        return self.left_masker.colliding(self.right_masker)

