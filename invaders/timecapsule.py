from flyer import InvadersFlyer


class TimeCapsule(InvadersFlyer):
    def __init__(self, time, added_flyer, removed_flyer=None):
        self.to_add = added_flyer
        self.to_remove = removed_flyer
        self.time = time

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def interact_with(self, other, fleets):
        other.interact_with_timecapsule(self, fleets)

    def tick(self, delta_time, fleets):
        self.time -= delta_time
        if self.time <= 0:
            fleets.remove(self)
            fleets.append(self.to_add)
            if self.to_remove:
                fleets.remove(self.to_remove)
