

class CastResult:
    pass


class EmptyCastResult(CastResult):
    pass


class Raycaster:
    def __init__(self):
        pass

    def cast(self, x):
        return EmptyCastResult()