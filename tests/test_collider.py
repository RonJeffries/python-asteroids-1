import pygame.mask
import pytest
from pygame import Surface

from Collider import Collider
from bitmap_maker import BitmapMaker


class Thing:
    def __init__(self, rect, mask):
        self.rect = rect
        self.mask = mask

    @property
    def position(self):
        return self.rect.center

    @position.setter
    def position(self, value):
        self.rect.center = value


class TestCollider:
    @pytest.fixture
    def make_probe(self):
        probe = Surface((1, 1))
        probe.set_colorkey((0, 0, 0))
        probe.set_at((0, 0), "white")
        probe_mask = pygame.mask.from_surface(probe)
        return probe, probe_mask

    @pytest.fixture
    def make_target(self):
        target = Surface((3, 3))
        target.set_colorkey((0, 0, 0))
        target.set_at((1, 1), "white")
        target_mask = pygame.mask.from_surface(target)
        return target, target_mask

    def test_idea(self, make_target, make_probe):
        target, target_mask = make_target
        probe, probe_mask = make_probe
        offset = (0, 0)
        assert not target_mask.overlap(probe_mask, offset)
        offset = (1, 1)
        assert target_mask.overlap(probe_mask, offset)

    def test_big_rect_center(self, make_target):
        target, _target_mask = make_target
        target_rect = target.get_rect()
        target_rect.center = (200, 200)
        assert target_rect.topleft == (199, 199)

    def test_small_rect_center(self, make_probe):
        probe, _probe_mask = make_probe
        probe_rect = probe.get_rect()
        probe_rect.center = (100, 100)
        assert probe_rect.topleft == (100, 100)

    def test_creation(self, make_target, make_probe):
        target_object = self.make_target_object(make_target)
        probe_object = self.make_probe_object(make_probe)
        collider = Collider(target_object, probe_object)

    def test_not_colliding(self, make_target, make_probe):
        target_object = self.make_target_object(make_target)
        probe_object = self.make_probe_object(make_probe)
        collider = Collider(target_object, probe_object)
        assert not collider.colliding()

    def test_colliding(self, make_target, make_probe):
        target_object = self.make_target_object(make_target)
        probe_object = self.make_probe_object(make_probe)
        probe_object.rect.center = (1, 1)
        collider = Collider(target_object, probe_object)
        assert collider.colliding()

    def make_probe_object(self, make_probe):
        probe, probe_mask = make_probe
        probe_object = Thing(probe.get_rect(), probe_mask)
        return probe_object

    def make_target_object(self, make_target):
        target, target_mask = make_target
        target_object = Thing(target.get_rect(), target_mask)
        return target_object


