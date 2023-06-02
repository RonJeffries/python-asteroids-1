# test timer object

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

    def test_with_method(self):
        checker = Checker(19)
        another = Checker(9)
        some_value = 31
        timer = Timer(1, checker.set)
        timer2 = Timer(1, another.set)
        timer.tick(1.1, 31)
        assert checker.happened == 31 + 19
        timer2.tick(1.1, 21)
        assert another.happened == 21 + 9

    def test_tick_args(self):
        result = ""

        def action(tick_arg):
            nonlocal result
            result = tick_arg
            return True

        timer = Timer(1, action)
        timer.tick(1.1, "tick arg")
        assert result == "tick arg"

    def test_tick_with_function(self):
        result = ""

        def action(arg):
            nonlocal result
            result = arg

        timer = Timer(1)
        timer.tick(1.1, action, "hello")
        assert result == "hello"

    def test_slicing(self):
        args = ("a", "b", "c")
        args_len = len(args)
        parms = ("F", "d", "e")
        all = args + parms
        assert all == ("a", "b", "c", "F", "d", "e")
        func = all[args_len]
        assert func == "F"
        first_args = all[:args_len]
        assert first_args == args
        last_args = all[args_len+1:]
        assert last_args == ("d", "e")



