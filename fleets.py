# SpaceObjects
from itertools import chain

from asteroid import Asteroid
from interactor import Interactor
from ship import Ship


class Fleets:
    def __init__(self):
        self.flyers = list()

    @property
    def all_objects(self):
        return self.flyers.copy()

    # adds and removes

    def add_flyer(self, flyer):
        self.flyers.append(flyer)

    def remove_flyer(self, flyer):
        if flyer in self.flyers:
            self.flyers.remove(flyer)

    def clear(self):
        self.flyers.clear()

    def cycle(self, delta_time, screen):
        self.update(delta_time)
        self.perform_interactions()
        self.tick(delta_time)
        self.draw(screen)

    def draw(self, screen):
        for flyer in self.all_objects:
            flyer.draw(screen)

    def update(self, delta_time):
        for flyer in self.all_objects:
            flyer.update(delta_time, self)

    def select(self, condition):
        return [flyer for flyer in self.all_objects if condition(flyer)]

    def tick(self, delta_time):
        for flyer in self.all_objects:
            flyer.tick(delta_time, self)

    def perform_interactions(self):
        Interactor(self).perform_interactions()

    def begin_interactions(self):
        for flyer in self.all_objects:
            flyer.begin_interactions(self)

    def end_interactions(self):
        for flyer in self.all_objects:
            flyer.end_interactions(self)
