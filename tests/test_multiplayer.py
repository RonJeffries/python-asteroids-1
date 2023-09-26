from asteroids.scorekeeper import ScoreKeeper
from asteroids.signal import Signal


class TestMultiPlayer():

    def test_signal(self):
        assert Signal(0).signal == 0
        assert Signal(1).signal == 1

    def test_keeper_scoring_inits_properly(self):
        assert ScoreKeeper(0)._scoring
        assert not ScoreKeeper(1)._scoring

    def test_keeper_switches_scoring(self):
        k0 = ScoreKeeper(0)
        k1 = ScoreKeeper(1)
        assert k0._scoring
        assert not k1._scoring
        s1 = Signal(1)
        k0.interact_with_signal(s1, [])
        k1.interact_with_signal(s1, [])
        assert not k0._scoring
        assert k1._scoring
        s0 = Signal(0)
        k0.interact_with_signal(s0, [])
        k1.interact_with_signal(s0, [])
        assert k0._scoring
        assert not k1._scoring
