from pygame import Vector2

from invaders.ImageMasher import Masker


class Collider:
    def __init__(self, left, right):
        try:
            self.left_collider = left._sprite
            self.right_collider = right._sprite
        except AttributeError:
            self.left_collider = Masker(left.mask, left.position)
            self.right_collider = Masker(right.mask, right.position)

    def colliding(self):
        return self.left_collider.colliding(self.right_collider)

