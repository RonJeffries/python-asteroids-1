from core import coin
from flyer import InvadersFlyer
from invaders.invader_player import InvaderPlayer
from invaders.reserveplayer import ReservePlayer
from invaders.timecapsule import TimeCapsule


class PlayerMaker(InvadersFlyer):
    def __init__(self):
        self.reserve = ReservePlayer(-999)
        self.final_action = self.final_deal_with_missing_player
        self.reserve_action = self.reserve_absent_game_over

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def interact_with(self, other, fleets):
        other.interact_with_playermaker(self, fleets)

    def begin_interactions(self, _fleets):
        self.reserve = ReservePlayer(-999)
        self.final_action = self.final_deal_with_missing_player
        self.reserve_action = self.reserve_absent_game_over

    def interact_with_invaderplayer(self, _player, _fleets):
        self.final_action = self.final_do_nothing

    def interact_with_reserveplayer(self, reserve, _fleets):
        self.reserve = self.reserve.rightmost_of(reserve)
        self.reserve_action = self.reserve_give_player_another_turn

    def end_interactions(self, fleets):
        self.final_action(fleets)

    def final_deal_with_missing_player(self, fleets):
        self.reserve_action(fleets)

    def final_do_nothing(self, fleets):
        pass

    def reserve_absent_game_over(self, fleets):
        coin.slug(fleets)

    def reserve_give_player_another_turn(self, fleets):
        fleets.remove(self)
        delay_until_new_player = 2.0
        a_bit_longer = 0.1
        self.provide_new_player(delay_until_new_player, fleets)
        self.provide_new_maker(delay_until_new_player + a_bit_longer, fleets)

    def provide_new_player(self, delay, fleets):
        player_capsule = TimeCapsule(delay, InvaderPlayer(), self.reserve)
        fleets.append(player_capsule)

    def provide_new_maker(self, delay, fleets):
        maker_capsule = TimeCapsule(delay, PlayerMaker())
        fleets.append(maker_capsule)

