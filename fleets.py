# SpaceObjects
from typing import Callable

import pygame

import u
from interactor import Interactor


class Fleets:
    def __init__(self):
        self.flyers = list()
        self.reminders = []

    @property
    def all_objects(self):
        return self.flyers.copy()

    # adds and removes

    def append(self, flyer):
        self.flyers.append(flyer)

    def remove(self, flyer):
        # more pythonic?
        try:
            self.flyers.remove(flyer)
        except ValueError:
            pass

    def clear(self):
        self.flyers.clear()

    def cycle(self, delta_time, screen):
        self.update(delta_time)
        self.perform_interactions()
        self.tick(delta_time)
        self.draw(screen)

    def draw(self, screen):
        # pygame.draw.circle(screen, "white", u.CENTER, u.SAFE_EMERGENCE_DISTANCE, 1)
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
        self.reminders = []
        for flyer in self.all_objects:
            flyer.begin_interactions(self)

    def end_interactions(self):
        for flyer in self.all_objects:
            self._execute_reminders()
            flyer.end_interactions(self)

    def remind_me(self, reminder: Callable, *args):
        reminder = [reminder, args]
        self.reminders.append(reminder)

    def _execute_reminders(self):
        for reminder in self.reminders:
            func = reminder[0]
            args = reminder[1]
            func(*args)
        self.reminders = []

