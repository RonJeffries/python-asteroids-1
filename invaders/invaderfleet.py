from pygame import Vector2

import u
from flyer import InvadersFlyer
from invaders.invader_group import InvaderGroup, CycleStatus


class InvaderFleet(InvadersFlyer):
    def __init__(self):
        self.step = Vector2(8, 0)
        self.down_step = Vector2(0, 32)
        self.invader_group = InvaderGroup()
        self.origin = Vector2(u.SCREEN_SIZE / 2 - 5*64, 512)
        self.invader_group.position_all_invaders(self.origin)
        self.direction = 1
        self.step_origin()

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    @property
    def testing_only_invaders(self):
        return self.invader_group.invaders

    def invader_count(self):
        return self.invader_group.invader_count()

    def update(self, delta_time, _fleets):
        result = self.invader_group.update_next(self.origin)
        self.process_result(result)

    def process_result(self, result):
        if result == CycleStatus.CONTINUE:
            pass
        elif result == CycleStatus.NEW_CYCLE:
            self.step_origin()
        elif result == CycleStatus.REVERSE:
            self.reverse_travel()

    def step_origin(self):
        self.origin = self.origin + self.direction * self.step

    def reverse_travel(self):
        self.direction = -self.direction
        self.origin = self.origin + self.direction * self.step + self.down_step

    def draw(self, screen):
        self.invader_group.draw(screen)

    def interact_with_playershot(self, shot, fleets):
        self.invader_group.interact_with_playershot(shot, fleets)

    def interact_with(self, other, fleets):
        other.interact_with_invaderfleet(self, fleets)
