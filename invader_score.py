from flyer import InvadersFlyer


class InvaderScore(InvadersFlyer):
    def __init__(self, score):
        self.score = score

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def interact_with(self, other, fleets):
        other.interact_with_invaderscore(self)
