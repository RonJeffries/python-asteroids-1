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
        timer = Timer(delay)
        assert not happened
        timer.tick(0.1, it_happened)
        assert not happened
        timer.tick(3, it_happened)
        assert happened

    def test_reset(self):
        happened = False

        def action():
            nonlocal happened
            happened = True
            return True

        delay = 1
        timer = Timer(delay)
        assert not happened
        timer.tick(1, action)
        assert happened
        assert timer.elapsed == 0

    def test_returning_none_resets_timer(self):
        happened = False

        def action_without_return():
            nonlocal happened
            happened = True

        delay = 1
        timer = Timer(delay)
        timer.tick(1.5, action_without_return)
        assert happened

    def test_with_method(self):
        checker = Checker(19)
        another = Checker(9)
        some_value = 31
        timer = Timer(1)
        timer2 = Timer(1)
        timer.tick(1.1, checker.set, 31)
        assert checker.happened == 31 + 19
        timer2.tick(1.1, another.set, 21)
        assert another.happened == 21 + 9

    def test_tick_args(self):
        result = ""

        def action(tick_arg):
            nonlocal result
            result = tick_arg
            return True

        timer = Timer(1)
        timer.tick(1.1, action, "tick arg")
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
        parameters = ("F", "d", "e")
        both = args + parameters
        assert both == ("a", "b", "c", "F", "d", "e")
        func = both[args_len]
        assert func == "F"
        first_args = both[:args_len]
        assert first_args == args
        last_args = both[args_len+1:]
        assert last_args == ("d", "e")



