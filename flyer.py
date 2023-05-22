
from abc import ABC, abstractmethod


class Flyer(ABC):

    @abstractmethod
    def interact_with(self, other, fleets):
        pass

    @abstractmethod
    def tick(self, delta_time, fleet, fleets):
        pass

