import pytest

from flyer import AsteroidFlyer, InvadersFlyer


def just_pass():
    pass


def get_subclasses(klass):
    for subclass in klass.__subclasses__():
        yield from get_subclasses(subclass)
        yield subclass


class TestFlyer:

    # @pytest.mark.skip("needs updating")
    def test_all_interact_with_implemented_in_asteroid_flyer(self):
        self.check_class(AsteroidFlyer)

    # @pytest.mark.skip("needs updating")
    def test_all_interact_with_implemented_in_invaders_flyer(self):
        self.check_class(InvadersFlyer)

    def check_class(self, test_class):
        subclasses = get_subclasses(test_class)
        ignores = ["BeginChecker", "EndChecker", "TimeCapsule", "PlayerExplosion", "ReservePlayer"]
        subclasses = [klass for klass in subclasses if klass.__name__ not in ignores]
        attributes = dir(test_class)
        pass_code = just_pass.__code__.co_code
        for klass in subclasses:
            name = klass.__name__.lower()
            self.check_top_class_has_interact_with_each_subclass(attributes, name, test_class)
            self.check_interact_with_present_and_not_just_pass(klass, name, pass_code)

    def check_top_class_has_interact_with_each_subclass(self, attributes, name, test_class):
        required_method = "interact_with_" + name
        if not required_method in attributes:
            print(test_class.__name__ + " does not implement " + required_method)
            assert False

    def check_interact_with_present_and_not_just_pass(self, klass, name, pass_code):
        if "interact_with" in klass.__dict__:
            interact_with_method = klass.__dict__["interact_with"]
            interact_with_code = interact_with_method.__code__.co_code
            if not interact_with_code != pass_code:
                print(name + " has pass in interact_with")
                assert False
        else:
            print(name + " does not implement `interact_with`")
            assert False

    def test_should_interact_with(self):
        # a subclass xyz of Flyer can implement
        # should_interact_with to return a list of classes
        # each of which will be checked for implementing
        # interact_with_xyz
        subclasses = get_subclasses(AsteroidFlyer)
        # print()
        # for k in sorted(subclasses, key=lambda klass: klass.__name__):
        #     print(k.__name__)
        # assert False
        for klass in subclasses:
            required_method = "interact_with_" + klass.__name__.lower()
            if "should_interact_with" in klass.__dict__:
                should_interact = klass.should_interact_with()
                for interactor in should_interact:
                    if required_method not in interactor.__dict__:
                        assert False, interactor.__name__ + " does not implement " + required_method

