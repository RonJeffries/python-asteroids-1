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
