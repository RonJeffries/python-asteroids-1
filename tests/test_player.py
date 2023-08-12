from invader_player import InvaderPlayer


class TestPlayer:
    def test_left_edge(self):
        player = InvaderPlayer()
        player.move(-10000)
        assert player.rect.centerx == player.left

    def test_right_edge(self):
        player = InvaderPlayer()
        player.move(10000)
        assert player.rect.centerx == player.right

