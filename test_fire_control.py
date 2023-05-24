

class FireControl:
    def __init__(self, number_of_missiles):
        self.number_of_missiles = number_of_missiles
        self.missile_tally = 0

    def begin_tally(self):
        self.missile_tally = 0

    def tally(self):
        self.missile_tally += 1

    @property
    def can_fire(self):
        return self.missile_tally < self.number_of_missiles


class TestFireControl:
    def test_class(self):
        FireControl(4)

    def test_can_fire(self):
        fc = FireControl(4)
        fc.begin_tally()
        fc.tally()
        assert fc.can_fire
        fc.tally()
        assert fc.can_fire
        fc.tally()
        assert fc.can_fire
        fc.tally()
        assert not fc.can_fire

