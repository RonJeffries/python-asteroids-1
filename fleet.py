# Fleet

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
