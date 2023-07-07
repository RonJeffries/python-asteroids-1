from pygame import Vector2

import u
from fleets import Fleets
from hyperspace_generator import HyperspaceGenerator
from ship import Ship
from tests.tools import FI


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

    def test_failure(self):
        fleets = Fleets()
        impossible = Vector2(-5, -9)
        ship = Ship(impossible)
        fi = FI(fleets)
        fleets.append(ship)
        hg = HyperspaceGenerator(ship)
        hg.recharge()
        hg.press_button(0, fleets, 45)  # fail = roll > 44 + tally
        assert fi.fragments

    def test_success(self):
        fleets = Fleets()
        impossible = Vector2(-5, -9)
        ship = Ship(impossible)
        fi = FI(fleets)
        fleets.append(ship)
        hg = HyperspaceGenerator(ship)
        hg.recharge()
        hg.press_button(0, fleets, 44)  # fail = roll > 44 + tally
        assert not fi.explosions

    def test_recharge_timer(self):
        fleets = Fleets()
        impossible = Vector2(-5, -9)
        ship = Ship(impossible)
        fi = FI(fleets)
        fleets.append(ship)
        hg = HyperspaceGenerator(ship)
        hg.press_button(0, fleets, 44)  # fail = roll > 44 + tally
        assert self.did_not_enter_hyperspace(impossible, ship)
        hg.tick(u.SHIP_HYPERSPACE_RECHARGE_TIME)
        hg.lift_button()
        hg.press_button(0, fleets, 44)  # fail = roll > 44 + tally
        assert self.did_enter_hyperspace(impossible, ship)

    def test_hyperspace_failure(self):
        # hyperspace fails when random(0 through 62) > asteroid count plus 44
        hg = HyperspaceGenerator(None)
        self.check_no_fail(hg, 0, 0)
        self.check_fail(hg, 45, 0)  # 45 > 44 you lose
        self.check_fail(hg, 62, 17)  # 62 > 44+ 17 you lose
        self.check_no_fail(hg, 62, 18)  # 62 !> 44+18 = 62

    @staticmethod
    def check_no_fail(hg, roll, asteroids):
        assert not hg.hyperspace_failed(asteroids, roll)

    @staticmethod
    def check_fail(hg, roll, asteroids):
        assert hg.hyperspace_failed(asteroids, roll)



