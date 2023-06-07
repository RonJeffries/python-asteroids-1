
import random

from pygame import Vector2

import u


class HyperspaceGenerator:
    def __init__(self, ship):
        self._charged = False
        self._button_down = False
        self._ship = ship
        self._asteroid_tally = 0

    def press_button(self, asteroid_tally):
        self._asteroid_tally = asteroid_tally
        if self._charged and not self._button_down:
            self.hyperspace_jump()
        self._button_down = True

    def hyperspace_jump(self):
        self._charged = False
        x = random.randrange(u.SCREEN_SIZE)
        y = random.randrange(u.SCREEN_SIZE)
        self._ship.move_to(Vector2(x, y))
        self._ship._angle = random.randrange(360)
        dx = random.randrange(u.SHIP_HYPERSPACE_MAX_VELOCITY)
        dy = random.randrange(u.SHIP_HYPERSPACE_MAX_VELOCITY)
        self._ship.accelerate_to(Vector2(dx, dy))

    def recharge(self):
        self._charged = True

    def lift_button(self):
        self._button_down = False
