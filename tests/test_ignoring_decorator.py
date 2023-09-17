from abc import ABC, abstractmethod, ABCMeta

import pytest


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

# Decorator Style


class ignoring_decorator(object):
    def __init__(self, names):
        print("ig init", names, "done")
        self.names = names

    def __call__(self, klass):
        print("call args", klass, "done")
        if self.names:
            for name in self.names:
                setattr(klass, name, lambda *args: None)
        return klass


# def ignoring_decorator(*outer):
#     print("inside decorator", outer)
#
#     def function(*args):
#         print("inside func", args, "done")
#     return function

# @ignoring_decorator
@ignoring_decorator(["bar"])
class FooDecorated(Base):
    def __init__(self):
        print("Foo init")

    def foo(self):
        return "foo"

    def baz(self):
        return "baz"


class TestIgnoringDecorator:
    def test_class_decorator(self):
        print("decorating")

        @ignoring_decorator(None)
        class Fubar:
            def action(self):
                return 4422
        print("calling")
        fubar = Fubar()
        assert fubar.action() == 4422
        foo = FooDecorated()
        assert foo.foo() == "foo"
        assert foo.bar() is None
        assert foo.baz() == "baz"
        with pytest.raises(NotImplementedError):
            foo.qux()