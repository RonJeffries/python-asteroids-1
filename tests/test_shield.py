import pytest
from pygame import Vector2

from invaders.shield import Shield


class TestShield:
    def test_exists(self):
        Shield(Vector2(0, 0))

    @pytest.mark.skip(reason="needs work")
    def test_mask_updates_after_shield_hit(self):
        pass

    @pytest.mark.skip(reason="good learning experience")
    def test_erase_and_blit_to_show_how_they_work_in_shield(self):
        pass


