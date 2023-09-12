import coin
from flyer import InvadersFlyer
from invader_player import InvaderPlayer
from timecapsule import TimeCapsule


class PlayerMaker(InvadersFlyer):
    def __init__(self):
        self.reserve = None
        self.player_missing = True

    def begin_interactions(self, _fleets):
        self.reserve = None
        self.player_missing = True

    def interact_with_invaderplayer(self, _player, _fleets):
        self.player_missing = False

    def interact_with_reserveplayer(self, reserve, _fleets):
        if not self.reserve:
            self.reserve = reserve
        elif reserve.reserve_number > self.reserve.reserve_number:
            self.reserve = reserve

    def end_interactions(self, fleets):
        if self.player_missing:
            if self.reserve:
                fleets.remove(self)
                capsule = TimeCapsule(2, InvaderPlayer(), self.reserve)
                fleets.append(capsule)
                fleets.append(TimeCapsule(2.1, PlayerMaker()))
            else:
                coin.slug(fleets)

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

    def interact_with_invadershot(self, shot, fleets):
        pass

    def interact_with_playerexplosion(self, explosion, fleets):
        pass

    def interact_with_playershot(self, shot, fleets):
        pass

    def interact_with_invaderexplosion(self, explosion, fleets):
        pass

    def interact_with_shield(self, shield, fleets):
        pass

    def interact_with_shotcontroller(self, controller, fleets):
        pass

    def interact_with_shotexplosion(self, bumper, fleets):
        pass

    def interact_with_topbumper(self, top_bumper, fleets):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_playermaker(self, fleets)

    def draw(self, screen):
        pass

    def tick(self, delta_time, fleets):
        pass

