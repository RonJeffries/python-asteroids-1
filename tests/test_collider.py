import pygame.mask
import pytest
from pygame import Surface


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
