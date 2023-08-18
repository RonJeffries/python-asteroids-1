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
        subclasses = get_subclasses(AsteroidFlyer)
        ignores = ["BeginChecker", "EndChecker"]
        subclasses = [klass for klass in subclasses if klass.__name__ not in ignores]
        attributes = dir(AsteroidFlyer)
        pass_code = just_pass.__code__.co_code
        for klass in subclasses:
            name = klass.__name__.lower()
            required_method = "interact_with_" + name
            assert required_method in attributes
            if "interact_with" in klass.__dict__:
                interact_with_method = klass.__dict__["interact_with"]
                interact_with_code = interact_with_method.__code__.co_code
                assert interact_with_code != pass_code, name + " has pass in interact_with"
            else:
                assert False, name + " does not implement `interact_with`"


    # @pytest.mark.skip("needs updating")
    def test_all_interact_with_implemented_in_invaders_flyer(self):
        test_class = InvadersFlyer
        subclasses = get_subclasses(test_class)
        ignores = []
        subclasses = [klass for klass in subclasses if klass.__name__ not in ignores]
        attributes = dir(test_class)
        pass_code = just_pass.__code__.co_code
        for klass in subclasses:
            name = klass.__name__.lower()
            print("checking", name)
            required_method = "interact_with_" + name
            assert required_method in attributes, "InvadersFlyer does not implement " + required_method
            if "interact_with" in klass.__dict__:
                interact_with_method = klass.__dict__["interact_with"]
                interact_with_code = interact_with_method.__code__.co_code
                assert interact_with_code != pass_code, name + " has pass in interact_with"
            else:
                assert False, name + " does not implement `interact_with`"

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

