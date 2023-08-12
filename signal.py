from flyer import AsteroidFlyer


class Signal(AsteroidFlyer):

    def __init__(self, signal):
        self.signal = signal

    def interact_with(self, other, fleets):
        other.interact_with_signal(self, fleets)

    def tick(self, delta_time, fleets):
        fleets.remove(self)

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

