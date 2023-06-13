from flyer import Flyer


def just_pass():
    pass


class TestFlyer:
    def test_all_interact_with_implemented_in_flyer(self):
        subclasses = Flyer.__subclasses__()
        ignores = ["BeginChecker", "EndChecker"]
        subclasses = [klass for klass in subclasses if klass.__name__ not in ignores]
        attributes = dir(Flyer)
        pass_code = just_pass.__code__.co_code
        for klass in subclasses:
            name = klass.__name__.lower()
            required_method = "interact_with_" + name
            assert required_method in attributes
            interact_with_method = klass.interact_with
            interact_with_code = interact_with_method.__code__.co_code
            assert interact_with_code != pass_code, name + " has pass in interact_with"
