import pytest

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

    def test_delay(self):
        player = TonePlayer()
        assert player.delay(55) == 0x34

    @pytest.mark.parametrize("invaders,delay", [(55, 0x34), (49, 0x2E), (0x11, 0x18), (0, 0x05), (-8, 0x05)])
    def test_delays(self, invaders, delay):
        player = TonePlayer()
        assert player.delay(invaders) == delay

