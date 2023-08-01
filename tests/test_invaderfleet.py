from pygame import Vector2

from bumper import Bumper
from invader import Invader
from invaderfleet import InvaderFleet


class TestInvaderFleet:
    def test_exists(self):
        fleet = InvaderFleet()

    def test_makes_invaders(self):
        fleet = InvaderFleet()
        invaders = fleet.invaders
        assert len(invaders) == 55

    def test_invaders_order(self):
        fleet = InvaderFleet()
        count = 0
        for x in range(11):
            for y in range(5):
                invader = fleet.invaders[count]
                assert invader.x == x
                assert invader.y == y
                count += 1

    def test_bumper_invader_collision(self):
        fleet = InvaderFleet()
        bumper_x = 16
        bumper = Bumper(bumper_x)
        invader_column = 5
        invader = Invader(invader_column, 2)
        start = Vector2(64, 512)
        step = 64
        invader.draw(None, start, step)
        invader.interact_with_bumper(bumper, fleet)
        assert not fleet.reverse
        start_x = bumper_x - invader_column*step
        start = Vector2(start_x, 512)
        invader.draw(None, start, step)
        invader.interact_with_bumper(bumper, fleet)
        assert fleet.reverse


