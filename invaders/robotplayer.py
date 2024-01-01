from pygame import Vector2

import u
from flyer import InvadersFlyer
from invaders.player_explosion import PlayerExplosion
from invaders.player_shot import PlayerShot
from invaders.sprite import Spritely, Sprite
from sounds import player


class RobotPlayer(Spritely, InvadersFlyer):
    shield_locations = ((198, 286), (378, 466), (558, 646), (738, 826))
    open_locations = (range(0, 198), range(287, 378), range(467, 558), range(647, 738), range(827, 1024))

    def __init__(self):
        self._sprite = Sprite.player()
        self.position = Vector2(u.INVADER_PLAYER_LEFT, u.INVADER_PLAYER_Y)

        self._free_to_fire = True
        self.invader_x_values = []

    def begin_interactions(self, fleets):
        self.invader_x_values = []
        self._free_to_fire = True

    def interact_with_destructor(self, destructor, fleets):
        self.explode(fleets)

    def interact_with_playershot(self, shot, fleets):
        self._free_to_fire = False

    def interact_with_invaderfleet(self, fleet, fleets):
        self.invader_x_values = fleet.invader_x_values()

    def interact_with_invadershot(self, shot, fleets):
        if self.colliding(shot):
            self.explode(fleets)

    def interact_with(self, other, fleets):
        other.interact_with_robotplayer(self, fleets)

    def is_in_open(self, x):
        return any([x in r for r in self.open_locations])

    def select_values_in_open(self, x_values):
        in_any_open = [x for x in x_values if self.is_in_open(x)]
        return in_any_open

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
            return u.INVADER_STEP
        elif starting_x > target_x:
            return -u.INVADER_STEP
        else:
            return 0

    def fire_when_ready(self, fleets):
        if self._free_to_fire:
            fleets.append(PlayerShot(self._sprite.center))

    def explode(self, fleets):
        frac = u.screen_fraction(self.position.x)
        player.play_stereo("explosion", frac)
        fleets.append(PlayerExplosion(self.position))
        fleets.remove(self)
