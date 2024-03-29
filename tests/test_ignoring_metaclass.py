from abc import ABC, abstractmethod

import pytest

from core.ignorethese import IgnoreThese


class AbstractClass(ABC):
    @abstractmethod
    def must(self):
        pass


class Base(ABC):

    def must(self):
        pass

    def foo(self):
        raise NotImplementedError

    def bar(self):
        raise NotImplementedError

    def baz(self):
        raise NotImplementedError

    def qux(self):
        raise NotImplementedError


class FooIgnores(Base, metaclass=IgnoreThese, ignore=["bar", "baz"]):
    def foo(self):
        return "foo"

    def baz(self):
        return "baz"


ignore_dict = {"bar": lambda *args: None, "baz": lambda *args: None}
CoveringClass = type("FooViaType", (Base,), ignore_dict)

# Function Style

class FooCovered(CoveringClass):
    def foo(self):
        return "foo"

    def baz(self):
        return "baz"


def ignore_these(klass, bases, names):
    dict = {name: lambda *args: None for name in names}
    cover = type("cover", bases, dict)
    klass.__bases__ = (cover,)


class FooFunction(Base):
    def foo(self):
        return "foo"

    def baz(self):
        return "baz"


ignore_these(FooFunction, (Base,), ["bar", "baz"])


class TestIgnoringMetaclass:
    def test_create(self):
        foo = FooIgnores()
        assert foo.foo() == "foo"
        assert foo.bar() is None
        assert foo.baz() == "baz"
        with pytest.raises(NotImplementedError):
            foo.qux()

    def test_using_covering(self):
        foo = FooCovered()
        assert foo.foo() == "foo"
        assert foo.bar() is None
        assert foo.baz() == "baz"
        with pytest.raises(NotImplementedError):
            foo.qux()

    def test_covering_function(self):
        foo = FooFunction()
        assert foo.foo() == "foo"
        assert foo.bar() is None
        assert foo.baz() == "baz"
        with pytest.raises(NotImplementedError):
            foo.qux()



