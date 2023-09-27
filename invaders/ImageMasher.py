from pygame import Vector2


class Masker:
    def __init__(self, mask, position):
        self.mask = mask.copy()  # don't mutate your input
        self.rect = mask.get_rect()
        self.rect.center = position

    @property
    def topleft(self):
        return Vector2(self.rect.topleft)

    def erase(self, masker):
        self.mask.erase(masker.mask, self.offset(masker))

    def colliding(self, masker):
        return self.rectangles_collide(masker) and self.masks_collide(masker)

    def rectangles_collide(self, masker):
        return self.rect.colliderect(masker.rect)

    def masks_collide(self, masker):
        return self.mask.overlap(masker.mask, self.offset(masker))

    def offset(self, masker):
        return masker.topleft - self.topleft

    def get_mask(self):
        return self.mask


class ImageMasher:
    @classmethod
    def from_flyers(cls, target, shot):
        target_masker = Masker(target.mask, target.position)
        shot_masker = Masker(shot.mask, shot.position)
        explosion_masker = Masker(shot.explosion_mask, shot.position)
        return cls(target_masker, shot_masker, explosion_masker)

    def __init__(self, target_masker, shot_masker, explosion_masker):
        self.target_masker = target_masker
        self.shot_masker = shot_masker
        self.explosion_masker = explosion_masker

    def determine_damage(self):
        self.erase_shot()
        self.erase_explosion()

    def erase_shot(self):
        self.target_masker.erase(self.shot_masker)

    def erase_explosion(self):
        self.target_masker.erase(self.explosion_masker)

    def get_new_mask(self):
        return self.target_masker.mask

    def update(self, mask, surface):
        self.determine_damage()
        self.apply_damage_to_surface(surface)
        return self.get_new_mask(), surface

    def apply_damage_to_surface(self, surface):
        new_mask = self.get_new_mask()
        for x in range(new_mask.get_rect().width):
            for y in range(new_mask.get_rect().height):
                bit = new_mask.get_at((x, y))
                if not bit:
                    surface.set_at((x, y), (0, 0, 0))
