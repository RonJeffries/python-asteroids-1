import u
from flyer import Flyer
from saucer import Saucer
from timer import Timer


class SaucerMaker(Flyer):

    def __init__(self):
        self._timer = Timer(u.SAUCER_EMERGENCE_TIME)
        self._saucer_gone = True
        self._scorekeeper = None

    def create_saucer(self, fleets):
        if self._scorekeeper and self._scorekeeper.score >= u.SAUCER_SCORE_FOR_SMALL:
            saucer = Saucer.small()
        else:
            saucer = Saucer.large()
        fleets.append(saucer)

    def begin_interactions(self, fleets):
        self._saucer_gone = True

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        self._saucer_gone = False

    def interact_with_scorekeeper(self, keeper, fleets):
        self._scorekeeper = keeper

    def interact_with_ship(self, ship, fleets):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_saucermaker(self, fleets)

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleets):
        if self._saucer_gone:
            self._timer.tick(delta_time, self.create_saucer, fleets)
