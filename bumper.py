from pygame import Rect

import u
from flyer import Flyer


class Bumper(Flyer):
    def __init__(self, x, incoming_direction):
        self.rect = Rect(x, 0, x+1, u.SCREEN_SIZE)
        self.incoming_direction = incoming_direction

    def interact_with_invaderfleet(self, invader, fleets):
        pass

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_bumper(self, fleets)

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleets):
        pass

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass
