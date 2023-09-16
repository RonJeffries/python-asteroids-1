from abc import ABC, abstractmethod

import pytest

from flyer import InvadersFlyer
from ignorethese import IgnoreThese


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


class FlyerIgnores(InvadersFlyer):
    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderfleet(self, fleet, fleets):
        pass

    def interact_with_invaderplayer(self, player, fleets):
        pass

    def interact_with_invadershot(self, shot, fleets):
        pass

    def interact_with_playerexplosion(self, explosion, fleets):
        pass

    def interact_with_playershot(self, shot, fleets):
        pass

    def interact_with_invaderexplosion(self, explosion, fleets):
        pass

    def interact_with_shield(self, shield, fleets):
        pass

    def interact_with_shotcontroller(self, controller, fleets):
        pass

    def interact_with_shotexplosion(self, bumper, fleets):
        pass

    def interact_with_topbumper(self, top_bumper, fleets):
        pass

    def interact_with(self, other, fleets):
        pass

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleets):
        pass


class TestIgnoringMetaclass:
    def test_create(self):
        foo = FooIgnores()
        assert foo.foo() == "foo"
        assert foo.bar() is None
        assert foo.baz() == "baz"
        with pytest.raises(NotImplementedError):
            foo.qux()
