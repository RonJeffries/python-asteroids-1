# Fleet
from timer import Timer


class Fleet:
    def __init__(self, flyers):
        self.flyers = flyers

    def __iter__(self):
        return self.flyers.copy().__iter__()

    def append(self, flyer):
        self.flyers.append(flyer)

    def remove(self, flyer):
        if flyer in self.flyers: self.flyers.remove(flyer)

    def draw(self, screen):
        for flyer in self:
            flyer.draw(screen)

    def tick(self, delta_time, fleets):
        result = True
        for flyer in self:
            result = result and flyer.tick(delta_time, self, fleets)
        return result


class ShipFleet(Fleet):
    def __init__(self, flyers):
        super().__init__(flyers)


class SaucerFleet(Fleet):
    def __init__(self, flyers):
        super().__init__(flyers)
        self.timer = Timer(u.SAUCER_EMERGENCE_TIME, self.bring_in_saucer)

    def bring_in_saucer(self, saucer):
        saucer.ready()
        self.flyers.append(saucer)

