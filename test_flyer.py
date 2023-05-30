from flyer import Flyer

_RETURN_NONE = (lambda: None).__code__.co_code


class TestFlyer:
    def test_all_interact_with_implemented_in_flyer(self):
        sc = Flyer.__subclasses__()
        ignores = ["BeginChecker", "EndChecker"]
        sc = [klass for klass in sc if klass.__name__ not in ignores]
        attrs = dir(Flyer)
        for klass in sc:
            name = klass.__name__.lower()
            method = "interact_with_" + name
            assert method in attrs
            iw = klass.interact_with
            iw_code = iw.__code__.co_code
            assert iw_code != _RETURN_NONE, name + " has pass in interact_with"
