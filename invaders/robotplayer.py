from pygame import Vector2

import u
from flyer import InvadersFlyer
from invaders.player_shot import PlayerShot
from invaders.sprite import Spritely, Sprite


class RobotPlayer(Spritely, InvadersFlyer):

    def __init__(self):
        self._sprite = Sprite.player()
        self.step = 4
        half_width = self._sprite.width / 2
        self.left = 64 + half_width
        self.right = 960 - half_width
        self.position = Vector2(self.left, u.INVADER_PLAYER_Y)
        self.count = 0
        self.invader_x_values = []
        self._can_shoot = True

    shield_locations = ((198, 286), (378, 466), (558, 646), (738, 826))
    open_locations = (range(0, 198), range(287, 378), range(467, 558), range(647, 738), range(827, 1024))

    def is_in_open(self, x):
        return any([x in r for r in self.open_locations])

    def select_values_in_open(self, x_values):
        in_any_open = [x for x in x_values if self.is_in_open(x)]
        return in_any_open

    def x_distance(self, position_vector):
        return abs(self.position.x - position_vector.x)

    def begin_interactions(self, fleets):
        self.invader_x_values = []
        self._can_shoot = True

    def interact_with_invaderfleet(self, fleet, fleets):
        self.invader_x_values = fleet.invader_x_values()

    def interact_with_playershot(self, shot, fleets):
        self._can_shoot = False

    def interact_with(self, other, fleets):
        other.interact_with_robotplayer(self, fleets)

    def nearest_invader_x(self, starting_x, x_values):
        possibles = self.select_values_in_open(x_values)
        if not possibles:
            return starting_x
        best_x = possibles[0]
        for x in possibles:
            if abs(starting_x - x) < abs(starting_x - best_x):
                best_x = x
        return best_x

    def update(self, delta_time, fleets):
        self.move_toward_target()
        self.fire_when_ready(fleets)

    def move_toward_target(self):
        starting_x = self.position.x
        step_x = self.get_step_toward_target(starting_x)
        self.move_along_x(starting_x, step_x)

    def get_step_toward_target(self, starting_x):
        target_x = self.nearest_invader_x(starting_x, self.invader_x_values)
        step_x = self.one_step_toward_target(starting_x, target_x)
        return step_x

    def move_along_x(self, starting_x, step_x):
        centerx = starting_x + step_x
        self.position = Vector2(centerx, self.position.y)

    def one_step_toward_target(self, starting_x, target_x):
        if starting_x < target_x:
            return self.step
        elif starting_x > target_x:
            return -self.step
        else:
            return 0

    def fire_when_ready(self, fleets):
        if self._can_shoot:
            fleets.append(PlayerShot(self._sprite.center))
