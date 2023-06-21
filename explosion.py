import random
from fragment import Fragment


class Explosion:

    @classmethod
    def from_ship(cls,position, fleets=None):
        simple = Fragment.simple_fragment
        vee = Fragment.v_fragment
        guy = Fragment.astronaut_fragment
        explosion = cls(position, [vee, guy, simple, simple, simple, simple, simple])
        if fleets:
            explosion.explosion_at(position, fleets)
            explosion.fragment_factory_methods = []
        return explosion

    @classmethod
    def from_saucer(cls,position, fleets=None):
        simple = Fragment.simple_fragment
        vee = Fragment.v_fragment
        explosion = cls(position, [vee, vee, simple, vee, simple, vee, simple])
        if fleets:
            explosion.explosion_at(position, fleets)
            explosion.fragment_factory_methods = []
        return explosion

    def __init__(self, position, fragment_factory_methods):
        self.position = position
        self.fragment_factory_methods = fragment_factory_methods

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
        fleets.append(fragment)
