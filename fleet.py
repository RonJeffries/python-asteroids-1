# Fleet
import u
from asteroid import Asteroid
from saucer import Saucer
from ship import Ship
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

    def extend(self, list):
        self.flyers.extend(list)

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
    ships_remaining = u.SHIPS_PER_QUARTER
    game_over = False

    def __init__(self, flyers):
        super().__init__(flyers)
        self.ship_timer = Timer(u.SHIP_EMERGENCE_TIME, self.spawn_ship_when_ready)
        ShipFleet.ships_remaining = u.SHIPS_PER_QUARTER

    def spawn_ship_when_ready(self, fleets):
        if not self.ships_remaining:
            ShipFleet.game_over = True
            return True
        if self.safe_to_emerge(fleets):
            self.append(Ship(u.CENTER))
            ShipFleet.ships_remaining -= 1
            return True
        else:
            return False

    def safe_to_emerge(self, fleets):
        if len(fleets.missiles) > 0:
            return False
        if len(fleets.saucer_missiles) > 0:
            return False
        return self.asteroids_far_enough_away(fleets.asteroids)

    def asteroids_far_enough_away(self, asteroids):
        for asteroid in asteroids:
            if asteroid.position.distance_to(u.CENTER) < u.SAFE_EMERGENCE_DISTANCE:
                return False
        return True

    def tick(self, delta_time, fleets):
        ships = fleets.ships
        if len(ships) == 0:
            self.ship_timer.tick(delta_time, fleets)
        super().tick(delta_time, fleets)
        return True


class SaucerFleet(Fleet):
    def __init__(self, flyers):
        super().__init__(flyers)
        self.timer = Timer(u.SAUCER_EMERGENCE_TIME, self.bring_in_saucer)

    def bring_in_saucer(self, fleets):
        self.flyers.append(Saucer())
        return True

    def tick(self, delta_time, fleets):
        super().tick(delta_time, fleets)
        if not self.flyers:
            self.timer.tick(delta_time, fleets)
        return True


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
