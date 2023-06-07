
import random

from pygame import Vector2

import u
from fleets import Fleets


class HyperspaceGenerator:
    def __init__(self, ship):
        self._charged = False
        self._button_down = False
        self._ship = ship
        self._asteroid_tally = 0

    def press_button(self, asteroid_tally, dice_roll=0, fleets=None):
        fleets = fleets if fleets else Fleets()
        self._asteroid_tally = asteroid_tally
        if self._charged and not self._button_down:
            self.jump_or_explode(asteroid_tally, dice_roll, fleets)
        self._button_down = True

    def jump_or_explode(self, asteroid_tally, dice_roll, fleets):
        if self.hyperspace_failed(asteroid_tally, dice_roll):
            print("exploding", dice_roll, "<",  asteroid_tally)
            self._ship.explode(fleets)
        else:
            print("jumping")
            self.hyperspace_jump()

    @staticmethod
    def hyperspace_failed(asteroid_tally, dice_roll):
        return dice_roll > 44 + asteroid_tally

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
