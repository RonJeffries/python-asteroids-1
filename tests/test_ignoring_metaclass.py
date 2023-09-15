import pytest

from ignorethese import IgnoreThese


class Base():
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


class TestIgnoringMetaclass:
    def test_create(self):
        foo = FooIgnores()
        assert foo.foo() == "foo"
        assert foo.bar() is None
        assert foo.baz() == "baz"
        with pytest.raises(NotImplementedError):
            foo.qux()
