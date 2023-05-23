import random

from flyer import Flyer
from fragment import Fragment


class Explosion(Flyer):
    def __init__(self, position):
        self.position = position

    def interact_with(self, other, fleets):
        pass

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleet, fleets):
        fleets.remove_flyer(self)
        self.explosion_at(self.position, fleets)

    def explosion_at(self, position, fleets):
        simple = Fragment.simple_fragment
        vee = Fragment.v_fragment
        guy = Fragment.astronaut_fragment
        fragment_factory_methods = [vee, guy, simple, simple, simple, simple, simple]
        random.shuffle(fragment_factory_methods)
        how_many = len(fragment_factory_methods)
        for i in range(how_many):
            factory_method = fragment_factory_methods[i]
            base_direction = 360 * i / how_many
            self.make_fragment(factory_method, base_direction, fleets)

    def make_fragment(self, factory_method, base_direction, fleets):
        twiddle = random.randrange(-20, 20)
        fragment = factory_method(position=self.position, angle=base_direction+twiddle)
        fleets.add_flyer(fragment)
