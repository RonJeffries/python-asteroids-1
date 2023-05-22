
from abc import ABC, abstractmethod


class Flyer(ABC):

    @abstractmethod
    def interact_with(self, other, fleets):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def tick(self, delta_time, fleet, fleets):
        pass

    # concrete methods, inheritable
    # so sue me

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_score(self, score, fleets):
        pass

    def interact_with_scorekeeper(self, scorekeeper, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass

