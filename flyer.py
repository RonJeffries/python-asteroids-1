
from abc import ABC, abstractmethod


class Flyer(ABC):

    @abstractmethod
    def interact_with(self, other, fleets):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def tick(self, delta_time, fleets):
        pass

    @abstractmethod
    def interact_with_asteroid(self, asteroid, fleets):
        pass

    @abstractmethod
    def interact_with_fragment(self, fragment, fleets):
        pass

    @abstractmethod
    def interact_with_missile(self, missile, fleets):
        pass

    @abstractmethod
    def interact_with_saucer(self, saucer, fleets):
        pass

    @abstractmethod
    def interact_with_ship(self, ship, fleets):
        pass

    # concrete methods, inheritable
    # so sue me

    def begin_interactions(self, fleets):
        pass

    def end_interactions(self, fleets):
        pass

    def interact_with_gameover(self, game_over, fleets):
        pass

    def interact_with_score(self, score, fleets):
        pass

    def interact_with_scorekeeper(self, scorekeeper, fleets):
        pass

    def interact_with_saucermaker(self, saucermaker, fleets):
        pass

    def interact_with_shipmaker(self, shipmaker, fleets):
        pass

    def interact_with_thumper(self, thumper, fleets):
        pass

    def interact_with_wavemaker(self, wavemaker, fleets):
        pass

    def update(self, delta_time, fleets):
        pass


