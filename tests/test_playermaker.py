from core.fleets import Fleets
from invaders.invader_player import InvaderPlayer
from invaders.invaders_game_over import InvadersGameOver
from invaders.playermaker import PlayerMaker
from invaders.reserveplayer import ReservePlayer
from tests.tools import FakeFleets


class TestPlayerMaker:
    def test_exists(self):
        PlayerMaker()

    def test_captures_reserve(self):
        maker = PlayerMaker()
        maker.interact_with_reserveplayer(ReservePlayer(1), None)
        maker.interact_with_reserveplayer(correct := ReservePlayer(2), None)
        maker.interact_with_reserveplayer(ReservePlayer(0), None)
        assert maker.reserve == correct
        maker.begin_interactions(None)
        assert maker.reserve.reserve_number < 0

    def test_notices_player(self):
        maker = PlayerMaker()
        maker.begin_interactions(None)
        final = maker.pluggable_final_action
        maker.interact_with_invaderplayer(None, None)
        assert maker.pluggable_final_action is not final

    def test_rezzes_time_capsule(self):
        maker = PlayerMaker()
        maker.begin_interactions(None)
        maker.interact_with_reserveplayer(ReservePlayer(0), None)
        maker.end_interactions(fleets := FakeFleets())
        assert fleets.appends
        capsule = fleets.appends[0]
        assert isinstance(capsule.to_add, InvaderPlayer)
        assert isinstance(capsule.to_remove, ReservePlayer)

    def test_game_over(self):
        maker = PlayerMaker()
        maker.begin_interactions(None)
        maker.end_interactions(fleets := Fleets())
        assert fleets.flyers
        assert any(isinstance(flyer, InvadersGameOver) for flyer in fleets.flyers)
