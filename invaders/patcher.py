class Patcher:

    @classmethod
    def nothing(cls, *args, **kwargs):
        pass

    @classmethod
    def turn_off(cls, obj, name):
        obj.__setattr__(name, cls.nothing)

    @classmethod
    def turn_on(cls, obj, name):
        if obj.__dict__.get(name):
            obj.__delattr__(name)
