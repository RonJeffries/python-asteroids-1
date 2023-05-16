from thumper import Thumper

thump = None


def beat1():
    global thump
    thump = 1


def beat2():
    global thump
    thump = 2


class TestThumper:
    def test_thumper_create(self):
        thumper = Thumper(beat1, beat2)
        assert thumper
        assert thumper._long_interval == 30/60
        assert thumper._short_interval == 8/60

    def test_thumper_thumps(self):
        """thumper ticks between 30 and 8 60ths"""
        thumper = Thumper(beat1, beat2)
        assert not thump
        thumper.tick(31/60)
        assert thump == 1
        thumper.tick(31/60)
        assert thump == 2
        thumper.tick(31/60)
        assert thump == 1

    def test_thumper_decrement_interval(self):
        thumper = Thumper(beat1, beat2)
        thumper.tick(128/60)
        assert thumper._interval == 30/60 - 1/60
        thumper.tick(128/60)
        assert thumper._interval == 30/60 - 1/60 - 1/60

    def test_thumper_countdown(self):
        thumper = Thumper(beat1, beat2)
        thumper._interval = 9/60
        thumper.tick(128/60)
        assert thumper._interval == 9/60 - 1/60
        thumper.tick(128/60)
        assert thumper._interval == 8/60
        thumper.tick(128/60)
        assert thumper._interval == 8/60

    def test_thumper_reset(self):
        thumper = Thumper(beat1, beat2)
        thumper._interval = 8/60
        thumper._execute_time = 2/60
        thumper._decrement_time = 2/60
        thumper.reset()
        assert thumper._interval == 30/60
        assert thumper._execute_time == 0
        assert thumper._decrement_time == 0


