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
        assert thumper._longest_time_between_beats == 30 / 60
        assert thumper._shortest_time_between_beats == 8 / 60

    def test_thumper_thumps(self):
        """thumper ticks between 30 and 8 60ths"""
        thumper = Thumper(beat1, beat2)
        thumper.interact_with_ship(None, None)
        thumper.interact_with_asteroid(None, None)
        assert not thump
        time = 31/60
        thumper.tick(31/60, None, None)
        assert thump == 1
        thumper.tick(31/60, None, None)
        assert thump == 2
        thumper.tick(31/60, None, None)
        assert thump == 1

    def test_thumper_decrement_interval(self):
        thumper = Thumper(beat1, beat2)
        thumper.interact_with_ship(None, None)
        thumper.interact_with_asteroid(None, None)
        thumper.tick(128/60, None, None)
        assert thumper._time_between_beats == 30 / 60 - 1 / 60
        thumper.tick(128/60, None, None)
        assert thumper._time_between_beats == 30 / 60 - 1 / 60 - 1 / 60

    def test_thumper_countdown(self):
        thumper = Thumper(beat1, beat2)
        thumper.interact_with_ship(None, None)
        thumper.interact_with_asteroid(None, None)
        thumper._time_between_beats = 9 / 60
        thumper.tick(128/60, None, None)
        assert thumper._time_between_beats == 9 / 60 - 1 / 60
        thumper.tick(128/60, None, None)
        assert thumper._time_between_beats == 8 / 60
        thumper.tick(128/60, None, None)
        assert thumper._time_between_beats == 8 / 60

    def test_thumper_reset(self):
        thumper = Thumper(beat1, beat2)
        thumper.interact_with_ship(None, None)
        thumper.interact_with_asteroid(None, None)
        thumper._time_between_beats = 8 / 60
        thumper._time_since_last_beat = 2 / 60
        thumper._time_since_last_decrement = 2 / 60
        thumper.reset()
        assert thumper._time_between_beats == 30 / 60
        assert thumper._time_since_last_beat == 0
        assert thumper._time_since_last_decrement == 0


