# test timer object

import pytest

from saucer import Saucer
from timer import Timer


class TestTimer():
    def test_creation(self):
        happened = False

        def it_happened():
            nonlocal happened
            happened = True
            return True
        delay = 3
        timer = Timer(delay, it_happened)
        assert not happened
        timer.tick(0.1)
        assert not happened
        timer.tick(3)
        assert happened

    def test_reset(self):
        happened = False

        def action():
            nonlocal happened
            happened = True
            return True
        delay = 1
        timer = Timer(delay, action)
        assert not happened
        timer.tick(1)
        assert happened
        assert timer.elapsed == 0

    def test_none_raises_exception(self):
        happened = False

        def action_without_return():
            nonlocal happened
            happened = True
        delay = 1
        timer = Timer(delay, action_without_return)
        with pytest.raises(Exception):
            timer.tick(1.5)
        assert happened

    def test_timer_with_args(self):
        saucer = Saucer()
        saucers = []

        def start_saucer(saucer, saucers):
            saucer.ready()
            saucers.append(saucer)
            return True
        delay = 1
        timer = Timer(delay, start_saucer, saucer, saucers)
        timer.tick(1.1)
        assert saucers
