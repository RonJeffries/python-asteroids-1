from invaders.tone_player import TonePlayer


class TestTonePlayer:
    def test_exists(self):
        TonePlayer()

    def test_tone_order(self):
        player = TonePlayer()
        assert player.next_tone() == "fastinvader4"
        assert player.next_tone() == "fastinvader1"
        assert player.next_tone() == "fastinvader2"
        assert player.next_tone() == "fastinvader3"
        assert player.next_tone() == "fastinvader4"
