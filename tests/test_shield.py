import pytest
from pygame import Vector2

from shield import Shield


class TestShield:
    def test_exists(self):
        Shield(Vector2(0, 0))

    @pytest.mark.skip(reason="needs work")
    def test_mask_updates_after_shield_hit(self):
        pass
