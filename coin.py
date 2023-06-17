from flyer import Flyer
from game_over import GameOver
from saucermaker import SaucerMaker
from scorekeeper import ScoreKeeper
from shipmaker import ShipMaker
from thumper import Thumper
from wavemaker import WaveMaker


class Coin(Flyer):

    @classmethod
    def quarter(cls):
        return cls(True, True)

    @classmethod
    def slug(cls):
        return cls(False, True)

    @classmethod
    def no_asteroids(cls):
        return cls(True, False)

    def __init__(self, is_quarter=True, want_asteroids=True):
        self.is_quarter = is_quarter
        self.want_asteroids = want_asteroids

    def interact_with(self, other, fleets):
        other.interact_with_coin(self, fleets)
    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_explosion(self, explosion, fleets):
        pass

    def interact_with_fragment(self, fragment, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucermissile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleets):
        fleets.clear()
        fleets.append(SaucerMaker())
        fleets.append(ScoreKeeper())
        fleets.append(Thumper())
        if self.want_asteroids:
            fleets.append(WaveMaker())
        fleets.append(ShipMaker() if self.is_quarter else GameOver())
