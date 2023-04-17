
import pygame
import pytest

from game import Game


class TestGame:
    def test_game_creation(self):
        game = Game()
        assert game