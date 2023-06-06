from pygame import Vector2

from hyperspace_generator import HyperspaceGenerator
from ship import Ship


class TestHyperspaceGenerator:
    def test_exists(self):
        ship = Ship(Vector2(0, 0))
        hg = HyperspaceGenerator(ship)

    def test_starts_discharged(self):
        ship = Ship(Vector2(0, 0))
        hg = HyperspaceGenerator(ship)
        assert not hg._charged

    def test_enters_hyperspace(self):
        impossible = Vector2(-5, -9)
        ship = Ship(impossible)
        hg = HyperspaceGenerator(ship)
        hg.recharge()
        hg.press_button()
        assert ship.position != impossible

    def test_next_entry_requires_recharge(self):
        impossible = Vector2(-5, -9)
        ship = Ship(impossible)
        hg = HyperspaceGenerator(ship)
        hg.press_button()
        ship.move_to(impossible)
        hg.press_button()
        assert ship.position == impossible
        hg.recharge()
        hg.press_button()
        assert ship.position != impossible
