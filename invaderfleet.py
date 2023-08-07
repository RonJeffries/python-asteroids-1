from pygame import Vector2

import u
from flyer import Flyer
from invader import Invader


class InvaderGroup():
    def __init__(self):
        self.invaders = ()
        self.create_invaders()

    def create_invaders(self):
        self.invaders = [Invader(x%11, x//11) for x in range(55)]

    def position_all_invaders(self, origin):
        for invader in self.invaders:
            invader.set_position(origin)

    def draw(self, screen):
        for invader in self.invaders:
            invader.draw(screen)

    def interact_with_bumper(self, bumper, fleet):
        for invader in self.invaders:
            invader.interact_with_bumper(bumper, fleet)

    def set_invader_position(self, index, origin):
        self.invaders[index].set_position(origin)


class InvaderFleet(Flyer):
    def __init__(self):
        self.step = Vector2(8, 0)
        self.down_step = Vector2(0, 32)

        self.invader_group = InvaderGroup()
        self.origin = Vector2(u.SCREEN_SIZE / 2 - 5*64, 512)
        self.invader_group.position_all_invaders(self.origin)

        self.reverse = False
        self.direction = 1

        self.next_invader = len(self.invader_group.invaders)

    @property
    def testing_only_invaders(self):
        return self.invader_group.invaders

    def end_interactions(self, fleets):
        pass

    def update(self, delta_time, _fleets):
        self.check_end_cycle(delta_time)
        self.invader_group.set_invader_position(self.next_invader, self.origin)
        self.next_invader += 1

    def check_end_cycle(self, delta_time):
        if self.next_invader >= len(self.invader_group.invaders):
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
        self.invader_group.draw(screen)

    def interact_with_bumper(self, bumper, _fleets):
        self.invader_group.interact_with_bumper(bumper, self)

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