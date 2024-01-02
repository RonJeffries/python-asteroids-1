from flyer import InvadersFlyer
from invaders.invader_player import InvaderPlayer
from invaders.invaders_game_over import InvadersGameOver
from invaders.reserveplayer import ReservePlayer
from invaders.robotplayer import RobotPlayer
from invaders.timecapsule import TimeCapsule


class PlayerMaker(InvadersFlyer):
    def __init__(self):
        self.reserve = ReservePlayer.invalid()
        self.player_found = None

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def interact_with(self, other, fleets):
        other.interact_with_playermaker(self, fleets)

    def begin_interactions(self, _fleets):
        self.reserve = ReservePlayer.invalid()
        self.player_found = None

    def interact_with_invaderplayer(self, player, _fleets):
        self.player_found = player

    def interact_with_reserveplayer(self, reserve, _fleets):
        self.reserve = self.reserve.rightmost_of(reserve)

    def interact_with_robotplayer(self, robot, fleets):
        self.player_found = robot

    def end_interactions(self, fleets):
        if not self.player_found:
            self.deal_with_missing_player(fleets)

    def deal_with_missing_player(self, fleets):
        if self.reserve.is_valid:
            self.reserve_give_player_another_turn(fleets)
        else:
            self.no_reserve_game_over(fleets)

    def no_reserve_game_over(self, fleets):
        fleets.append(InvadersGameOver())
        new_player = RobotPlayer()
        reserve_to_remove = None
        self.set_up_next_player(new_player, reserve_to_remove, fleets)

    def reserve_give_player_another_turn(self, fleets):
        new_player = InvaderPlayer()
        reserve_to_remove = self.reserve
        self.set_up_next_player(new_player, reserve_to_remove, fleets)

    def set_up_next_player(self, new_player, reserve_to_remove, fleets):
        delay_until_new_player = 2.0
        a_bit_longer = 0.1
        delay_until_new_maker = delay_until_new_player + a_bit_longer
        fleets.remove(self)
        player_capsule = TimeCapsule(delay_until_new_player, new_player, reserve_to_remove)
        fleets.append(player_capsule)
        maker = PlayerMaker()
        maker_capsule = TimeCapsule(delay_until_new_maker, maker)
        fleets.append(maker_capsule)

