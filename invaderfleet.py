from pygame import Vector2

import u
from flyer import InvadersFlyer
from invader_group import InvaderGroup


class InvaderFleet(InvadersFlyer):
    def interact_with_invaderfleet(self, bumper, fleets):
        pass

    def interact_with_invadershot(self, bumper, fleets):
        pass

    def interact_with_playershot(self, shot, fleets):
        self.invader_group.interact_with_playershot(shot)

    def __init__(self):
        self.step = Vector2(8, 0)
        self.down_step = Vector2(0, 32)

        self.invader_group = InvaderGroup()
        self.origin = Vector2(u.SCREEN_SIZE / 2 - 5*64, 512)
        self.invader_group.position_all_invaders(self.origin)
        self.reverse = False
        self.direction = 1
        self.step_origin()

    @property
    def testing_only_invaders(self):
        return self.invader_group.invaders

    def end_interactions(self, fleets):
        pass

    def update(self, delta_time, _fleets):
        result = self.invader_group.update_next(self.origin)
        self.process_result(result)

    def process_result(self, result):
        if result == "ok":
            pass
        elif result == "end":
            if self.reverse:
                self.reverse_travel()
            else:
                self.step_origin()
        else:
            assert False

    def step_origin(self):
        self.origin = self.origin + self.direction * self.step

    def reverse_travel(self):
        self.reverse = False
        self.direction = -self.direction
        self.origin = self.origin + self.direction * self.step + self.down_step


    def at_edge(self, bumper_incoming_direction):
        self.reverse = bumper_incoming_direction == self.direction

    def draw(self, screen):
        self.invader_group.draw(screen)

    def interact_with_bumper(self, bumper, _fleets):
        self.invader_group.interact_with_bumper(bumper, self)

    def interact_with_invaderplayer(self, player, fleet):
        pass

    def interact_with_playerexplosion(self, _explosion, _fleets):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_invaderfleet(self, fleets)

    def tick(self, delta_time, fleets):
        pass