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

    def test_sound_on_first_call(self):
        player = TonePlayer(FakeSoundPlayer())
        tone_played = player.play_tone(55)
        assert tone_played == "fastinvader4"

    def test_no_sound_on_second_call(self):
        player = TonePlayer(FakeSoundPlayer())
        tone_played = player.play_tone(55)
        tone_played = player.play_tone(55)
        assert tone_played is None

    def test_plays_in_correct_order(self):
        player = TonePlayer(FakeSoundPlayer())
        for correct in ["fastinvader4", "fastinvader1", "fastinvader2", "fastinvader3"]:
            assert player.play_tone(55) == correct
            player._elapsed_time += 99


class FakeSoundPlayer:
    def play_stereo(self, sound, frac):
        return sound
