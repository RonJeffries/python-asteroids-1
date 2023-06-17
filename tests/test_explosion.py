import u
from explosion import Explosion
from fleets import Fleets
from fragment import Fragment


class TestExplosion:
    def test_explosion(self):
        fleets = Fleets()
        explosion = Explosion.from_ship(u.CENTER)
        fleets.append(explosion)
        explosion.tick(0.1, fleets)
        mix = fleets.all_objects
        for o in mix:
            print(o, o is Fragment)
        assert explosion not in mix
        fragments = [f for f in mix if isinstance(f, Fragment)]
        assert len(fragments) == 7
