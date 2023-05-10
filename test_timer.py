# test timer object

import pytest

from saucer import Saucer
from timer import Timer


class Checker:
    def __init__(self, extra):
        self.happened = 0
        self.extra = extra if extra else 0

    def set(self, value):
        self.happened = value + self.extra
        return True


class TestTimer:
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

    def test_returning_none_resets_timer(self):
        happened = False

        def action_without_return():
            nonlocal happened
            happened = True

        delay = 1
        timer = Timer(delay, action_without_return)
        timer.tick(1.5)
        assert happened

    def test_timer_with_args(self):
        saucer = Saucer()
        saucers = []

        def start_saucer(a_saucer, the_saucers):
            a_saucer.ready()
            the_saucers.append(a_saucer)
            return True

        delay = 1
        timer = Timer(delay, start_saucer, saucer, saucers)
        timer.tick(1.1)
        assert saucers

    def test_with_method(self):
        checker = Checker(19)
        another = Checker(9)
        some_value = 31
        timer = Timer(1, checker.set, some_value)
        timer2 = Timer(1, another.set, 21)
        timer.tick(1.1)
        assert checker.happened == 31 + 19
        timer2.tick(1.1)
        assert another.happened == 21 + 9

    def test_tick_args(self):
        result = ""

        def action(action_arg, tick_arg):
            nonlocal result
            result = action_arg + " " + tick_arg
            return True

        timer = Timer(1, action, "action arg")
        timer.tick(1.1, "tick arg")
        assert result == "action arg tick arg"
