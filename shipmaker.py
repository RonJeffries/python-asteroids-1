import u
from flyer import Flyer
from ship import Ship
from timer import Timer


class ShipMaker(Flyer):
    def __init__(self):
        self._timer = Timer(u.SHIP_EMERGENCE_TIME, self.create_ship)
        self._need_ship = True

    def begin_interactions(self, fleets):
        self._need_ship = True

    def interact_with_ship(self, ship, fleets):
        self._need_ship = False

    def tick(self, delta_time, fleet, fleets):
        if self._need_ship:
            self._timer.tick(delta_time, fleets)

    def create_ship(self, fleets):
        fleets.add_ship(Ship(u.CENTER))

    def interact_with(self, other, fleets):
        pass

    def draw(self, screen):
        pass