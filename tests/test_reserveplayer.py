from reserveplayer import ReservePlayer


class TestReservePlayer:
    def test_exists(self):
        ReservePlayer(0)

    def test_first_position(self):
        player = ReservePlayer(0)
        rect = player.rect
        assert rect.centerx == 64 + rect.width // 2