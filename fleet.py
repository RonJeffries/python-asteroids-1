# Fleet

import u
from saucer import Saucer
from ship import Ship
from timer import Timer


class Fleet:
    def __init__(self, flyers):
        self.flyers = flyers

    def __bool__(self):
        return bool(self.flyers)

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

    def extend(self, list_of_flyers):
        self.flyers.extend(list_of_flyers)

    def remove(self, flyer):
        if flyer in self.flyers:
            self.flyers.remove(flyer)

    def draw(self, screen):
        for flyer in self:
            flyer.draw(screen)

    def tick(self, delta_time, fleets):
        for flyer in self:
            flyer.tick(delta_time, self, fleets)


class SaucerFleet(Fleet):
    def __init__(self, flyers):
        super().__init__(flyers)
        self.timer = Timer(u.SAUCER_EMERGENCE_TIME, self.bring_in_saucer)

    def bring_in_saucer(self, _fleets):
        self.flyers.append(Saucer())
        return True

    def tick(self, delta_time, fleets):
        super().tick(delta_time, fleets)
        if not self.flyers:
            self.timer.tick(delta_time, fleets)
        return True


class ShipFleet(Fleet):
    ships_remaining = u.SHIPS_PER_QUARTER
    game_over = False

    def __init__(self, flyers):
        super().__init__(flyers)
        self.ship_timer = Timer(u.SHIP_EMERGENCE_TIME, self.spawn_ship_when_ready)
        ShipFleet.ships_remaining = u.SHIPS_PER_QUARTER
        ShipFleet.game_over = False

    def spawn_ship_when_ready(self, fleets):
        if not self.ships_remaining:
            ShipFleet.game_over = True
            return True
        if fleets.safe_to_emerge():
            self.append(Ship(u.CENTER))
            ShipFleet.ships_remaining -= 1
            return True
        else:
            return False

    def tick(self, delta_time, fleets):
        if not fleets.ships:
            self.ship_timer.tick(delta_time, fleets)
        super().tick(delta_time, fleets)
        return True
