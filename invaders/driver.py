from pygame import Vector2

import u
from flyer import InvadersFlyer
from invaders.player_shot import PlayerShot
from invaders.sprite import Spritely, Sprite


class Driver(Spritely, InvadersFlyer):

    def __init__(self):
        self._sprite = Sprite.player()
        self.step = 4
        half_width = self._sprite.width / 2
        self.left = 64 + half_width
        self.right = 960 - half_width
        self.position = Vector2(self.left, u.INVADER_PLAYER_Y)
        self.count = 0
        self.invader_x_values = []

    shield_locations = ((198, 286), (378, 466), (558, 646), (738, 826))
    open_locations = (range(0, 198), range(287, 378), range(467, 558), range(647, 738), range(827, 1024))

    def is_in_open(self, x):
        return any([x in r for r in self.open_locations])

    def select_values_in_open(self, x_values):
        in_any_open = [x for x in x_values if self.is_in_open(x)]
        return in_any_open

    def nearest_invader_x(self, x_values):
        possibles = self.select_values_in_open(x_values)
        if not possibles:
            return self.position.x
        best_x = possibles[0]
        for x in possibles:
            if abs(self.position.x - x) < abs(self.position.x - best_x):
                best_x = x
        return best_x

    def x_distance(self, position_vector):
        return abs(self.position.x - position_vector.x)

    def begin_interactions(self, fleets):
        self.invader_x_values = []

    def interact_with_invaderfleet(self, fleet, fleets):
        self.invader_x_values = fleet.invader_x_values()

    def interact_with(self, other, fleets):
        other.interact_with_driver(self, fleets)

    def update(self, delta_time, fleets):
        target_x = self.nearest_invader_x(self.invader_x_values)
        self.take_one_step_toward_target(target_x)
        self.fire_when_ready(fleets)

    def fire_when_ready(self, fleets):
        self.count = (self.count + 1) % 60
        if not self.count:
            fleets.append(PlayerShot(self._sprite.center))

    def take_one_step_toward_target(self, target_x):
        step_x = self.one_step_toward_target(target_x)
        self.take_one_step(step_x)

    def take_one_step(self, step_x):
        centerx = self._sprite.centerx + step_x
        self.position = Vector2(centerx, self.position.y)

    def one_step_toward_target(self, target_x):
        step_x = 0
        if self._sprite.centerx < target_x:
            step_x = self.step
        elif self._sprite.centerx > target_x:
            step_x = -self.step
        return step_x
