import u
from flyer import Flyer
from saucer import Saucer
from timer import Timer


class SaucerMaker(Flyer):
    def __init__(self):
        self._timer = Timer(u.SAUCER_EMERGENCE_TIME, self.create_saucer)
        self._saucer_gone = True

    def create_saucer(self, fleets):
        fleets.add_saucer(Saucer())

    def begin_interactions(self, fleets):
        self._saucer_gone = True

    def interact_with_saucer(self, saucer, fleets):
        self._saucer_gone = False

    def interact_with(self, other, fleets):
        other.interact_with_saucermaker(self, fleets)

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleet, fleets):
        if self._saucer_gone:
            self._timer.tick(delta_time, fleets)
