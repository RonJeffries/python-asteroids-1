from core import coin
from flyer import InvadersFlyer
from invaders.invader_player import InvaderPlayer
from invaders.reserveplayer import ReservePlayer
from invaders.timecapsule import TimeCapsule


class PlayerMaker(InvadersFlyer):
    def __init__(self):
        self.reserve = None
        self.player_missing = True

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def interact_with(self, other, fleets):
        other.interact_with_playermaker(self, fleets)

    def begin_interactions(self, _fleets):
        self.reserve = None
        self.player_missing = True

    def interact_with_invaderplayer(self, _player, _fleets):
        self.player_missing = False

    def interact_with_reserveplayer(self, reserve, _fleets):
        self.remember_rightmost_reserve_player(reserve)

    def remember_rightmost_reserve_player(self, reserve: ReservePlayer):
        if not self.reserve:
            self.reserve = reserve
        elif reserve.is_to_the_right_of(self.reserve):
            self.reserve = reserve

    def end_interactions(self, fleets):
        if self.player_missing:
            if self.reserve:
                self.give_player_another_turn(fleets)
            else:
                self.game_over(fleets)

    def give_player_another_turn(self, fleets):
        fleets.remove(self)
        delay_until_new_player = 2.0
        a_bit_longer = 0.1
        self.provide_new_player(delay_until_new_player, fleets)
        self.provide_new_maker(delay_until_new_player + a_bit_longer, fleets)

    def provide_new_player(self, delay_until_new_player, fleets):
        player_capsule = TimeCapsule(delay_until_new_player, InvaderPlayer(), self.reserve)
        fleets.append(player_capsule)

    def provide_new_maker(self, delay_a_bit_longer, fleets):
        maker_capsule = TimeCapsule(delay_a_bit_longer, PlayerMaker())
        fleets.append(maker_capsule)

    def game_over(self, fleets):
        coin.slug(fleets)
