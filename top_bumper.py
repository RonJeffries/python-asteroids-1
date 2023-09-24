from flyer import InvadersFlyer


class TopBumper(InvadersFlyer):
    def __init__(self):
        self.y = 40

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def interact_with(self, other, fleets):
        other.interact_with_topbumper(self, fleets)

    def intersecting(self, point):
        return point.y <= self.y


