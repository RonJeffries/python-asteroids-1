from dataclasses import dataclass

class TestInvadersAI:

    def test_hookup(self):
        assert 2 + 2 == 4

    def test_dataclass(self):
        @dataclass
        class Perception:
            under_shield: bool = False
            under_invader: bool = False
            under_missile_left: bool = False
            under_missile_right: bool = False
            under_missile_center: bool = False
            at_right_edge: bool = False
            at_left_edge: bool = False

        p1 = Perception(True, False, False, False, False, False, False)
        p2 = Perception(True, False, False, False, False, False, False)
        p3 = Perception(True, True, False, False, False, False, False)
        assert p1 == p2
        assert p1 != p3
