from flyer import Flyer, InvadersFlyer


class TimeCapsule(InvadersFlyer):
    def interact_with_playermaker(self, maker, fleets):
        pass

    def interact_with_timecapsule(self, capsule, fleets):
        pass

    def __init__(self, time, added_flyer, removed_flyer=None):
        self.to_add = added_flyer
        self.to_remove = removed_flyer
        self.time = time

    def interact_with(self, other, fleets):
        other.interact_with_timecapsule(self, fleets)

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleets):
        self.time -= delta_time
        if self.time <= 0:
            fleets.remove(self)
            fleets.append(self.to_add)
            if self.to_remove:
                fleets.remove(self.to_remove)

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderfleet(self, fleet, fleets):
        pass

    def interact_with_invaderplayer(self, player, fleets):
        pass

    def interact_with_invadershot(self, shot, fleets):
        pass

    def interact_with_playerexplosion(self, explosion, fleets):
        pass

    def interact_with_playershot(self, shot, fleets):
        pass

    def interact_with_invaderexplosion(self, explosion, fleets):
        pass

    def interact_with_roadfurniture(self, shield, fleets):
        pass

    def interact_with_shotcontroller(self, controller, fleets):
        pass

    def interact_with_shotexplosion(self, bumper, fleets):
        pass

    def interact_with_topbumper(self, top_bumper, fleets):
        pass
