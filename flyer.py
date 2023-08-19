
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

    # not abstract FSR
    def update(self, delta_time, fleets):
        pass

    # concrete methods, inheritable
    # so sue me

    def begin_interactions(self, fleets):
        pass

    def end_interactions(self, fleets):
        pass


class InvadersFlyer(Flyer):

    @property
    @abstractmethod
    def mask(self):
        pass

    @property
    @abstractmethod
    def rect(self):
        pass

    @rect.setter
    def rect(self, value):
        pass

    @abstractmethod
    def interact_with_bumper(self, bumper, fleets):
        pass

    @abstractmethod
    def interact_with_invaderfleet(self, fleet, fleets):
        pass

    @abstractmethod
    def interact_with_invaderplayer(self, player, fleets):
        pass

    @abstractmethod
    def interact_with_invadershot(self, shot, fleets):
        pass

    @abstractmethod
    def interact_with_playerexplosion(self, explosion, fleets):
        pass

    @abstractmethod
    def interact_with_playershot(self, shot, fleets):
        pass

    # Inherited for convenience
    def interact_with_invaderexplosion(self, explosion, fleets):
        pass

    def interact_with_shotcontroller(self, controller, fleets):
        pass

    # @abstractmethod
    def interact_with_shotexplosion(self, bumper, fleets):
        pass

    def interact_with_topbumper(self, top_bumper, fleets):
        pass


class AsteroidFlyer(Flyer):

    @abstractmethod
    def interact_with_asteroid(self, asteroid, fleets):
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

    def interact_with_fragment(self, fragment, fleets):
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

    def interact_with_signal(self, signal, fleets):
        pass

    def interact_with_thumper(self, thumper, fleets):
        pass

    def interact_with_wavemaker(self, wavemaker, fleets):
        pass


