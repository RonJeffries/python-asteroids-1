import random

from flyer import Flyer
from fragment import Fragment


class Explosion(Flyer):
    @classmethod
    def from_ship(cls,position):
        simple = Fragment.simple_fragment
        vee = Fragment.v_fragment
        guy = Fragment.astronaut_fragment
        return cls(position, [vee, guy, simple, simple, simple, simple, simple])

    @classmethod
    def from_saucer(cls,position):
        simple = Fragment.simple_fragment
        vee = Fragment.v_fragment
        return cls(position, [vee, vee, simple, vee, simple, vee, simple])

    def __init__(self, position, fragment_factory_methods):
        self.position = position
        self.fragment_factory_methods = fragment_factory_methods

    def interact_with(self, other, fleets):
        other.interact_with_explosion(self, fleets)

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleets):
        fleets.remove_flyer(self)
        self.explosion_at(self.position, fleets)

    def explosion_at(self, _position, fleets):
        random.shuffle(self.fragment_factory_methods)
        how_many = len(self.fragment_factory_methods)
        for i in range(how_many):
            factory_method = self.fragment_factory_methods[i]
            base_direction = 360 * i / how_many
            self.make_fragment(factory_method, base_direction, fleets)

    def make_fragment(self, factory_method, base_direction, fleets):
        twiddle = random.randrange(-20, 20)
        fragment = factory_method(position=self.position, angle=base_direction+twiddle)
        fleets.add_flyer(fragment)
