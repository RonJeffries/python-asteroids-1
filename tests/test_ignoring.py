import pytest


class Ignorables():
    def __init__(self, ignores=[]):
        print(self.__class__.__dict__)
        for ign in ignores:
            if not ign in self.__class__.__dict__:
                print("no", ign)
                setattr(self, ign, self.none)
            else:
                print("not hammering ", ign)

    def none(self, o, f):
        pass

    def interact_with_bar(self, _object, _fleets):
        raise NotImplementedError

    def interact_with_baz(self, _object, _fleets):
        raise NotImplementedError

    def interact_with_qux(self, _object, _fleets):
        raise NotImplementedError


class Foo(Ignorables):
    ignore_list = ["interact_with_bar", "interact_with_qux"]

    def __init__(self):
        super().__init__(self.ignore_list)

    def abc(self, value):
        return 40 + value

    def interact_with_qux(self, thing, fleets):
        fleets.append(42)


class TestIgnoring:
    def test_exists(self):
        fleets = [36]
        assert 36 in fleets
        foo = Foo()
        assert foo.abc(2) == 42
        foo.interact_with_bar(33, [])
        with pytest.raises(NotImplementedError):
            foo.interact_with_baz(33, [])
        fleets = []
        foo.interact_with_qux(33, fleets)
        assert fleets[0] == 42

    def test_dict(self):
        dict = {"a": 1, "b": 2}
        assert "a" in dict
