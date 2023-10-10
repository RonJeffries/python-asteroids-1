from invaders.patcher import Patcher


class _Pluggable:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def turn_off_increment(self):
        Patcher.turn_off(self, "increment")

    def turn_on_increment(self):
        Patcher.turn_on(self, "increment")


class TestPluggable:
    def test_pluggable(self):
        p = _Pluggable()
        assert p.count == 0
        p.increment()
        assert p.count == 1
        p.turn_off_increment()
        p.increment()
        assert p.count == 1
        p.turn_on_increment()
        p.increment()
        assert p.count == 2
        p.turn_on_increment()
        p.increment()
        assert p.count == 3

    def test_two_instances(self):
        p1 = _Pluggable()
        p2 = _Pluggable()
        assert p1.count == 0
        assert p2.count == 0
        p1.turn_off_increment()
        p1.increment()
        p2.increment()
        assert p1.count == 0
        assert p2.count == 1

        p1.turn_on_increment()
        p2.turn_off_increment()
        p1.increment()
        p2.increment()
        assert p1.count == 1
        assert p2.count == 1
