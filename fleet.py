# Fleet
import u
from saucer import Saucer
from timer import Timer


class Fleet:
    def __init__(self, flyers):
        self.flyers = flyers

    def __iter__(self):
        return self.flyers.copy().__iter__()

    def __len__(self):
        return len(self.flyers)

    def __getitem__(self, item):
        return self.flyers[item]

    def append(self, flyer):
        self.flyers.append(flyer)

    def clear(self):
        self.flyers.clear()

    def extend(self, *args):
        self.flyers.extend(*args)

    def remove(self, flyer):
        if flyer in self.flyers: self.flyers.remove(flyer)

    def draw(self, screen):
        for flyer in self:
            flyer.draw(screen)

    def tick(self, delta_time, fleets):
        result = True
        for flyer in self:
            result = flyer.tick(delta_time, self, fleets) and result
        return result


class ShipFleet(Fleet):
    def __init__(self, flyers):
        super().__init__(flyers)


class SaucerFleet(Fleet):
    def __init__(self, flyers):
        super().__init__(flyers)
        self.timer = Timer(u.SAUCER_EMERGENCE_TIME, self.bring_in_saucer)

    def bring_in_saucer(self):
        self.flyers.append(Saucer())
        return True

    def tick(self, delta_time, fleets):
        super().tick(delta_time, fleets)
        if not self.flyers:
            self.timer.tick(delta_time)
        return True
