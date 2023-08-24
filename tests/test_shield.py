import pytest
from pygame import Vector2

from bitmap_maker import BitmapMaker
from fleets import Fleets
from invader_shot import InvaderShot
from shield import Shield
from tests.tools import FI


class TestShield:
    def test_exists(self):
        Shield(Vector2(0, 0))

    @pytest.mark.skip(reason="needs work")
    def test_mask_updates_after_shield_hit(self):
        pass


