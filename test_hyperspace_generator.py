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
        hg.press_button(99)
        assert self.did_enter_hyperspace(impossible, ship)

    @staticmethod
    def did_enter_hyperspace(impossible, ship):
        return ship.position != impossible

    @staticmethod
    def did_not_enter_hyperspace(impossible, ship):
        return ship.position == impossible

    def test_next_entry_requires_recharge_and_lift_button(self):
        impossible = Vector2(-5, -9)
        ship = Ship(impossible)
        hg = HyperspaceGenerator(ship)
        hg.recharge()
        hg.press_button(99)
        assert self.did_enter_hyperspace(impossible, ship)
        ship.move_to(impossible)
        hg.press_button(99)
        assert self.did_not_enter_hyperspace(impossible, ship)
        hg.recharge()
        hg.press_button(99)
        assert self.did_not_enter_hyperspace(impossible, ship)
        hg.lift_button()
        hg.press_button(99)
        assert self.did_enter_hyperspace(impossible, ship)
