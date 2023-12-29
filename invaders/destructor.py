from flyer import InvadersFlyer


class Destructor(InvadersFlyer):
    def __init__(self):
        pass

    def rect(self):
        return None

    def mask(self):
        return None

    def interact_with(self, other, fleets):
        other.interact_with_destructor(self, fleets)

    def end_interactions(self, fleets):
        fleets.remove(self)
