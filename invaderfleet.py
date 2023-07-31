from flyer import Flyer
from invader import Invader


class InvaderFleet(Flyer):
    def __init__(self):
        self.invaders = [Invader(x//5, x % 5) for x in range(55)]

    def draw(self, screen):
        pass

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass

    def interact_with(self, other, fleets):
        pass

    def tick(self, delta_time, fleets):
        pass