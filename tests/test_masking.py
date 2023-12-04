import pygame.mask
import pytest
from pygame import Surface, Vector2, Rect

from invaders.ImageMasher import ImageMasher, Masker
from invaders.bitmap_maker import BitmapMaker
from invaders.invader_shot import InvaderShot
from invaders.player_shot import PlayerShot
from invaders.sprite import Sprite
from tests.test_collider import Thing


class TestMasking:

    def check_bits(self, mask, hits):
        rect = mask.get_rect()
        ok = True
        print()
        actual_hits = []
        for y in range(rect.h):
            for x in range(rect.w):
                cell = (x, y)
                bit = mask.get_at(cell)
                if bit == 0:
                    actual_hits.append(cell)
                print(bit, end="")
                if cell in hits:
                    ok = ok and bit == 0
                else:
                    ok = ok and bit == 1
            print()
        print(actual_hits)
        assert ok

    def mask_from_string(self, data):
        data = data.strip()
        lines = data.split("\n")
        rows = len(lines)
        cols = len(lines[0])
        mask = pygame.Mask((cols, rows))
        for y in range(rows):
            line = lines[y].strip()
            for x in range(cols):
                char = line[x]
                mask.set_at((x, y), char == "1")
        return mask

    @pytest.fixture
    def make_missile(self):
        surf = Surface((3, 3))
        # ***
        #  *
        #  *
        surf.set_colorkey("black")
        surf.fill("white", surf.get_rect())
        surf.set_at((0, 1), "black")
        surf.set_at((0, 2), "black")
        # surf.set_at((1, 1), "black")
        surf.set_at((2, 1), "black")
        surf.set_at((2, 2), "black")
        mask = pygame.mask.from_surface(surf)
        return Thing(mask.get_rect(), mask)

    @pytest.fixture
    def make_target(self):
        surf = Surface((8, 8))
        surf.set_colorkey("black")
        surf.fill("white", surf.get_rect())
        mask = pygame.mask.from_surface(surf)
        return Thing(mask.get_rect(), mask)

    @pytest.fixture
    def make_explosion(self):
        mask = pygame.Mask((5, 5), fill=True)
        rect = pygame.Rect(0, 0, 5, 5)
        return Thing(rect, mask)

    @pytest.fixture
    def make_small_explosion(self):
        mask = pygame.Mask((3, 3), fill=True)
        rect = pygame.Rect(0, 0, 3, 3)
        return Thing(rect, mask)

    @pytest.fixture
    def make_x(self):
        data = """
        101
        010
        101
        """
        mask = self.mask_from_string(data)
        rect = pygame.Rect(0, 0, 3, 3)
        return Thing(rect, mask)

    @pytest.fixture
    def make_plus(self):
        data = """
        010
        111
        010
        """
        mask = self.mask_from_string(data)
        rect = pygame.Rect(0, 0, 3, 3)
        return Thing(rect, mask)

    @pytest.fixture
    def make_small_square(self):
        data = """
        111
        101
        111
        """
        mask = self.mask_from_string(data)
        rect = pygame.Rect(0, 0, 3, 3)
        return Thing(rect, mask)

    @pytest.fixture
    def make_square(self):
        data = """
        11111
        10001
        10001
        10001
        11111
        """
        mask = self.mask_from_string(data)
        rect = pygame.Rect(0, 0, 5, 5)
        return Thing(rect, mask)

    def test_what_are_centers(self, make_missile, make_target):
        missile = make_missile
        assert missile.rect.center == (1, 1)
        target = make_target
        assert target.rect.center == (4, 4)

    def test_raw_overlap(self, make_missile, make_target):
        missile = make_missile
        target = make_target
        overlap_mask = target.mask.overlap_mask(missile.mask, (0, 0))
        rect = overlap_mask.get_rect()
        assert rect.topleft == (0, 0)
        assert rect.w == 8
        assert rect.h == 8

    def test_empty_overlap(self, make_missile, make_target):
        missile = make_missile
        target = make_target
        overlap_mask: pygame.Mask = target.mask.overlap_mask(missile.mask, (7, -1))
        rect = overlap_mask.get_rect()
        assert rect.topleft == (0, 0)
        for x in range(rect.w):
            for y in range(rect.h):
                assert overlap_mask.get_at((x, y)) == 0

    def test_top_right_overlap(self, make_missile, make_target):
        missile = make_missile
        target = make_target
        overlap_mask: pygame.Mask = target.mask.overlap_mask(missile.mask, (6, -1))
        rect = overlap_mask.get_rect()
        assert rect.topleft == (0, 0)
        assert overlap_mask.get_at((7, 0)) == 1
        assert overlap_mask.get_at((7, 1)) == 1
        assert overlap_mask.get_at((7, 2)) == 0

    def test_center_overlap(self, make_missile, make_target):
        missile = make_missile
        target = make_target
        overlap_mask: pygame.Mask = target.mask.overlap_mask(missile.mask, (6, -1))
        rect = overlap_mask.get_rect()
        assert rect.topleft == (0, 0)
        assert overlap_mask.get_at((7, 0)) == 1
        assert overlap_mask.get_at((7, 1)) == 1
        assert overlap_mask.get_at((7, 2)) == 0

    def test_mask_rect_does_not_matter(self, make_missile, make_target):
        missile = make_missile
        target = make_target
        missile.rect.center = (20, 20)
        assert missile.rect.topleft == (19, 19)
        overlap_mask: pygame.Mask = target.mask.overlap_mask(missile.mask, (6, -1))
        rect = overlap_mask.get_rect()
        assert rect.topleft == (0, 0)
        assert overlap_mask.get_at((7, 0)) == 1
        assert overlap_mask.get_at((7, 1)) == 1
        assert overlap_mask.get_at((7, 2)) == 0

    def test_use_mask_rect_in_overlap(self, make_missile, make_target):
        missile = make_missile
        target = make_target
        missile.rect.center = (7, 0)
        assert missile.rect.topleft == (6, -1)
        assert target.rect.topleft == (0, 0)
        overlap_mask: pygame.Mask = target.mask.overlap_mask(missile.mask, missile.rect.topleft)
        rect = overlap_mask.get_rect()
        assert rect.topleft == (0, 0)
        assert overlap_mask.get_at((7, 0)) == 1
        assert overlap_mask.get_at((7, 1)) == 1
        assert overlap_mask.get_at((7, 2)) == 0

    def test_use_both_rects_in_overlap(self, make_missile, make_target):
        missile = make_missile
        target = make_target
        target.rect.center = (100, 200)
        assert target.rect.topleft == (100-4, 200-4)
        missile.rect.center = (103, 196)
        offset = Vector2(missile.rect.topleft) - Vector2(target.rect.topleft)
        assert offset == Vector2(6, -1)
        overlap_mask: pygame.Mask = target.mask.overlap_mask(missile.mask, offset)
        rect = overlap_mask.get_rect()
        assert rect == (0, 0, 8, 8)  # always relative
        assert rect.topleft == (0, 0)
        assert overlap_mask.get_at((7, 0)) == 1
        assert overlap_mask.get_at((7, 1)) == 1
        assert overlap_mask.get_at((7, 2)) == 0

        assert target.mask.get_at((7, 0)) == 1
        assert target.mask.get_at((7, 1)) == 1
        target.mask.erase(overlap_mask, (0, 0))
        assert target.mask.get_at((7, 0)) == 0
        assert target.mask.get_at((7, 1)) == 0

        explosion_mask = pygame.Mask((5, 5), fill=True)
        explosion_rect = explosion_mask.get_rect()
        explosion_rect.center = missile.rect.center

    def test_explosion_offset(self, make_missile, make_target, make_explosion):
        missile = make_missile
        missile.rect.center = (103, 196)
        target = make_target
        target.rect.center = (100, 200)
        explosion = make_explosion
        assert explosion.rect.center == (2, 2)
        targeting_offset = Vector2(missile.rect.topleft) - Vector2(target.rect.topleft)
        overlap_mask: pygame.Mask = target.mask.overlap_mask(missile.mask, targeting_offset)
        target.mask.erase(overlap_mask, (0, 0))
        hits = [(7, 0), (7, 1)]
        self.check_bits(target.mask, hits)

        target.mask.fill()
        self.check_bits(target.mask, [])
        explosion.rect.center = missile.rect.center  # hitting at same point
        offset = Vector2(explosion.rect.topleft) - Vector2(target.rect.topleft)
        assert offset == (5, -2)
        target.mask.erase(explosion.mask, offset)
        hits = [(5, 0), (5, 1), (5, 2), (6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2)]
        self.check_bits(target.mask, hits)

    def test_centers(self, make_missile, make_target):
        missile = make_missile
        target = make_target
        target.rect.center = (100, 200)
        missile.rect.center = (103, 196)
        offset = Vector2(missile.rect.topleft) - Vector2(target.rect.topleft)
        assert offset == (6, -1)
        explosion_rect = Rect(0, 0, 5, 5)
        explosion_center = explosion_rect.center
        assert explosion_center == (2, 2)
        explosion_rect.center = missile.rect.center
        mtl = Vector2(missile.rect.topleft)
        etl = Vector2(explosion_rect.topleft)
        assert missile.rect.topleft == (102, 195)
        assert explosion_rect.topleft == (101, 194)
        adjustment = etl - mtl
        assert adjustment == (-1, -1)

    def test_center_adjustment(self):
        m_center = (1, 1)  # 3x3 object
        e_center = (2, 2)  # 5x5 object
        center_adjustment = Vector2(m_center) - Vector2(e_center)
        assert center_adjustment == (-1, -1)

    def test_thing_from_bits(self):
        data = """
        10101010
        01010101
        10101010
        01010101
        10101010
        01010101
        10101010
        01010101
        """
        mask = self.mask_from_string(data)
        hits = []
        for y in range(8):
            for x in range(8):
                even = y % 2
                if x % 2 != even:
                    hits.append((x, y))
        self.check_bits(mask, hits)

    # ImageMasher tests start here

    def test_masher_exists(self, make_missile, make_target, make_small_explosion):
        shield = make_target
        shot = make_missile
        expl = make_small_explosion
        shot.explosion_mask = expl.mask
        ImageMasher.from_flyers(shield, shot)

    def test_masher_vs_shot(self, make_missile, make_target, make_small_explosion):
        shield = make_target
        shield.position = (100, 200)
        shot = make_missile
        shot.position = (100, 200)
        expl = make_small_explosion
        shot.explosion_mask = expl.mask
        assert shot.rect.center == (100, 200)
        masher = ImageMasher.from_flyers(shield, shot)
        masher.erase_shot()
        mask = masher.get_new_mask()
        hits = [(3, 3), (4, 3), (5, 3), (4, 4), (4, 5)]
        self.check_bits(mask, hits)

    def test_masher_both(self, make_missile, make_target, make_small_explosion):
        shield = make_target
        shield.position = (100, 200)
        shot = make_missile
        shot.position = (100, 200)
        expl = make_small_explosion
        shot.explosion_mask = expl.mask
        masher = ImageMasher.from_flyers(shield, shot)
        masher.determine_damage()
        mask = masher.get_new_mask()
        hits = [(3, 3), (4, 3), (5, 3), (3, 4), (4, 4), (5, 4), (3, 5), (4, 5), (5, 5)]
        self.check_bits(mask, hits)

    def test_shots_explosion_masks(self):
        player_shot = PlayerShot()
        assert isinstance(player_shot.explosion_mask, pygame.Mask)
        invader_shot = InvaderShot((0, 0), Sprite.squiggles())
        assert isinstance(invader_shot.explosion_mask, pygame.Mask)

    def test_plus_square(self, make_target, make_square, make_plus):
        x = make_square
        x.position = (100, 200)
        plus = make_plus
        plus.position = (100, 200)
        plus.explosion_mask = x.mask
        target = make_target
        target.position = (100, 200)
        masher = ImageMasher.from_flyers(target, plus)
        masher.erase_shot()
        masher.erase_explosion()
        mask = masher.get_new_mask()
        hits = [(2, 2), (3, 2), (4, 2), (5, 2), (6, 2),
                (2, 3), (4, 3), (6, 3),
                (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
                (2, 5), (4, 5), (6, 5),
                (2, 6), (3, 6), (4, 6), (5, 6), (6, 6)]
        self.check_bits(mask, hits)

    def test_masker_exists(self, make_plus):
        plus = make_plus
        masker = Masker(plus.mask, (100, 200))

    @pytest.fixture
    def five_mask(self):
        five_data = """
        11111
        11111
        11111
        11111
        11111
        """
        return self.mask_from_string(five_data)

    @pytest.fixture
    def three_mask(self):
        three_data = """
        111
        111
        111
        """
        return self.mask_from_string(three_data)

    @pytest.fixture
    def plus_mask(self):
        data = """
        010
        111
        010
        """
        return self.mask_from_string(data)

    def test_masker_centered(self, five_mask, three_mask):
        target = Masker(five_mask, (100, 200))
        bullet = Masker(three_mask, (100, 200))
        target.erase(bullet)
        erased = target.get_mask_testing_only()
        hits = [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3)]
        self.check_bits(erased, hits)

    def test_masker_down_right(self, five_mask, three_mask):
        target = Masker(five_mask, (100, 200))
        bullet = Masker(three_mask, (101, 201))
        target.erase(bullet)
        erased = target.get_mask_testing_only()
        hits = [(2, 2), (3, 2), (4, 2), (2, 3), (3, 3), (4, 3), (2, 4), (3, 4), (4, 4)]
        self.check_bits(erased, hits)

    def test_rectangle_collision(self, three_mask):
        target = Masker(three_mask, (100, 100))
        bullet = Masker(three_mask, (100, 100))
        assert target.rectangles_collide(bullet)
        bullet = Masker(three_mask, (102, 100))
        assert target.rectangles_collide(bullet)
        bullet = Masker(three_mask, (103, 100))
        assert not target.rectangles_collide(bullet)

    def test_mask_collision(self, three_mask, plus_mask):
        target = Masker(three_mask, (100, 100))
        bullet = Masker(plus_mask, (100, 100))
        assert target.masks_collide(bullet)
        bullet = Masker(plus_mask, (101, 101))
        assert target.masks_collide(bullet)
        bullet = Masker(plus_mask, (102, 102))
        assert not target.masks_collide(bullet)

    def test_masker_colliding(self, three_mask, plus_mask):
        target = Masker(three_mask, (100, 100))
        bullet = Masker(plus_mask, (100, 100))
        assert target.colliding(bullet)
        bullet = Masker(plus_mask, (101, 101))
        assert target.colliding(bullet)
        bullet = Masker(plus_mask, (102, 102))
        assert not target.colliding(bullet)
