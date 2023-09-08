from flyer import Flyer


class TimeCapsule(Flyer):
    def __init__(self, flyer, time):
        self.flyer = flyer
        self.time = time

    def interact_with(self, other, fleets):
        pass

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleets):
        self.time -= delta_time
        if self.time <= 0:
            fleets.remove(self)
            fleets.append(self.flyer)
