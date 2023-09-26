from invaders.reserveplayer import ReservePlayer


class TestReservePlayer:
    def test_exists(self):
        ReservePlayer(0)

    def test_first_position(self):
        player = ReservePlayer(0)
        rect = player.rect
        assert rect.centerx == self.first_position(rect)

    def test_second_position(self):
        player = ReservePlayer(1)
        rect = player.rect
        step_between_rps = rect.width + rect.width // 4
        assert rect.centerx == self.first_position(rect) + step_between_rps

    def first_position(self, rect):
        return 64 + rect.width // 2