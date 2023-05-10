# Fleet
import random

import u
from asteroid import Asteroid
from fragment import Fragment, VFragment
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
        result = True
        for flyer in self:
            result = flyer.tick(delta_time, self, fleets) and result
        return result


class AsteroidFleet(Fleet):
    def __init__(self, asteroids):
        super().__init__(asteroids)
        self.timer = Timer(u.ASTEROID_DELAY, self.create_wave)
        self.asteroids_in_this_wave = 2

    def create_wave(self):
        self.extend([Asteroid() for _ in range(0, self.next_wave_size())])

    def next_wave_size(self):
        self.asteroids_in_this_wave += 2
        if self.asteroids_in_this_wave > 10:
            self.asteroids_in_this_wave = 11
        return self.asteroids_in_this_wave

    def tick(self, delta_time, fleets):
        super().tick(delta_time, fleets)
        if not self.flyers:
            self.timer.tick(delta_time)
        return True


class ExplosionFleet(Fleet):
    def __init__(self):
        super().__init__([])

    def explosion_at(self, position):
        fragment_classes = [VFragment, VFragment, Fragment, Fragment, Fragment, Fragment, Fragment]
        how_many = len(fragment_classes)
        for i in range(how_many):
            fragment_class = fragment_classes[i]
            base_direction = 360 * i / how_many
            self.make_fragment(base_direction, fragment_class, position)

    def make_fragment(self, base_direction, fragment_class, position):
        twiddle = random.randrange(-20, 20)
        fragment = fragment_class(position=position, angle=base_direction + twiddle)
        self.flyers.append(fragment)


class MissileFleet(Fleet):
    def __init__(self, flyers, maximum_number_of_missiles):
        self.maximum_number_of_missiles = maximum_number_of_missiles
        super().__init__(flyers)

    def fire(self, callback, *args) -> bool:
        if len(self) < self.maximum_number_of_missiles:
            self.append(callback(*args))
            return True
        else:
            return False


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
