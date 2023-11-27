from flyer import InvadersFlyer
from invaders.invaders_saucer import InvadersSaucer
from invaders.timecapsule import TimeCapsule


class InvadersSaucerMaker(InvadersFlyer):
    def __init__(self):
        self.shot_count = None
        self.invader_count = None

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def interact_with(self, other, fleets):
        other.interact_with_invaderssaucermaker(self, fleets)

    def begin_interactions(self, fleets):
        self.shot_count = None
        self.invader_count = None

    def interact_with_invaderfleet(self, invader_fleet, fleets):
        self.invader_count = invader_fleet.invader_count()

    def interact_with_invaderplayer(self, invader_player, fleets):
        self.shot_count = invader_player.shot_count

    def end_interactions(self, fleets):
        if self.shot_count is not None and self.invader_count is not None and self.invader_count >= 8:
            fleets.append(InvadersSaucer(self.shot_count))
        fleets.remove(self)
        new_maker = InvadersSaucerMaker()
        fleets.append(TimeCapsule(10, new_maker))
