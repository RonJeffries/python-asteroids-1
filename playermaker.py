from invader_player import InvaderPlayer
from timecapsule import TimeCapsule


class PlayerMaker:
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
        if self.player_missing and self.reserve:
            capsule = TimeCapsule(2, InvaderPlayer(), self.reserve)
            fleets.append(capsule)

