from core.fleets import Fleets
from invaders.destructor import Destructor
from tests.tools import FI


class TestDestructor:
    def test_destructor_exits(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(destructor := Destructor())
        print(fleets.all_objects)
        assert fi.destructors
        destructor.end_interactions(fleets)
        assert not fi.destructors
