from pygame import Vector2

import u
from flyer import Flyer
from invader import Invader


class InvaderFleet(Flyer):
    def __init__(self):
        self.step = Vector2(8, 0)
        self.down_step = Vector2(0, 32)
        self.invaders = [Invader(x%11, x//11) for x in range(55)]
        self.reverse = False
        self.direction = 1
        self.origin = Vector2(u.SCREEN_SIZE / 2 - 5*64, 512)
        self.next_invader = len(self.invaders)
        self.position_all_invaders()

    def position_all_invaders(self):
        for invader in self.invaders:
            invader.set_position(self.origin)

    def end_interactions(self, fleets):
        pass

    def update(self, delta_time, _fleets):
        self.check_end_cycle(delta_time)
        self.invaders[self.next_invader].set_position(self.origin)
        self.next_invader += 1

    def check_end_cycle(self, delta_time):
        if self.next_invader >= len(self.invaders):
            self.reverse_or_continue(delta_time)

    def reverse_or_continue(self, delta_time):
        # we use +, not += because += modifies in place.
        if self.reverse:
            self.reverse = False
            self.direction = -self.direction
            self.origin = self.origin + self.direction * self.step + self.down_step
        else:
            self.origin = self.origin + self.direction * self.step
        self.next_invader = 0

    def at_edge(self, bumper_incoming_direction):
        self.reverse = bumper_incoming_direction == self.direction

    def draw(self, screen):
        for invader in self.invaders:
            invader.draw(screen)

    def interact_with_bumper(self, bumper, _fleets):
        for invader in self.invaders:
            invader.interact_with_bumper(bumper, self)

    def interact_with(self, other, fleets):
        pass

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass

    def tick(self, delta_time, fleets):
        pass