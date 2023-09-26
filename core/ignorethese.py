from abc import ABCMeta


class IgnoreThese(ABCMeta):

    @classmethod
    def __prepare__(metacls, name, bases, ignore=None):
        result = {}
        if ignore:
            for name in ignore:
                result[name] = lambda *args: None
        return result

    def __new__(cls, name, bases, classdict, ignore=None):
        result = type.__new__(cls, name, bases, dict(classdict))
        return result
