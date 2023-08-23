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

    def intersecting(self, point):
        return point.y <= self.y

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderexplosion(self, explosion, fleets):
        pass

    def interact_with_invaderfleet(self, bumper, fleets):
        pass

    def interact_with_invaderplayer(self, bumper, fleets):
        pass

    def interact_with_invadershot(self, bumper, fleets):
        pass

    def interact_with_playerexplosion(self, _explosion, _fleets):
        pass

    def interact_with_playershot(self, bumper, fleets):
        pass

    def interact_with_shotcontroller(self, controller, fleets):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_topbumper(self, fleets)

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleets):
        pass


