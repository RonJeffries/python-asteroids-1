from core.fleets import Fleets
from invaders.invader_player import InvaderPlayer
from invaders.invader_score import InvaderScoreKeeper
from invaders.invaderfleet import InvaderFleet
from invaders.invaders_saucer import InvadersSaucer
from invaders.player_shot import PlayerShot
from pygame import Vector2
from tests.tools import FI
import u


class TestInvadersSaucer:
    def test_exists(self):
        InvadersSaucer()

    def test_saucer_moves(self):
        saucer = InvadersSaucer()
        start = saucer.position
        fleets = Fleets()
        fleets.append(InvaderFleet())
        saucer.update(1.0/60.0, fleets)
        assert saucer.position.x != start.x

    def test_missing_shot(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(saucer := InvadersSaucer())
        shot = PlayerShot()
        shot.position = Vector2(0, 0)
        assert fi.invader_saucers
        saucer.interact_with_playershot(shot, fleets)
        assert fi.invader_saucers

    def test_dies_if_hit(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(saucer := InvadersSaucer())
        shot = PlayerShot()
        fleets.append(shot)
        shot.position = saucer.position
        assert fi.invader_saucers
        assert fi.player_shots
        saucer.interact_with_playershot(shot, fleets)
        shot.interact_with_invaderssaucer(saucer, fleets)
        assert not fi.invader_saucers
        assert not fi.player_shots

    def test_first_score(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(saucer := InvadersSaucer())
        fleets.append(keeper := InvaderScoreKeeper())
        fleets.append(player := InvaderPlayer())
        saucer.interact_with_invaderplayer(player, fleets)
        shot = PlayerShot()
        shot.position = saucer.position
        shot_count = 0

        def kill_saucer(expecting):
            nonlocal shot_count
            saucer._player_shot_count = shot_count
            shot_count += 1
            saucer.interact_with_playershot(shot, fleets)
            score = fi.scores[-1]
            assert score.score == expecting
            player.fire(fleets)
            saucer.interact_with_invaderplayer(player, fleets)
        kill_saucer(100)
        kill_saucer(50)
        kill_saucer(50)
        kill_saucer(100)

        kill_saucer(150)
        kill_saucer(100)
        kill_saucer(100)
        kill_saucer(50)

        kill_saucer(300)
        kill_saucer(100)
        kill_saucer(100)
        kill_saucer(100)

        kill_saucer(50)
        kill_saucer(150)
        kill_saucer(100)
        kill_saucer(100)

    def test_start_on_right(self):
        player = InvaderPlayer()
        player.shot_count = 0
        saucer = InvadersSaucer()
        saucer.interact_with_invaderplayer(player, [])
        saucer.end_interactions([])
        assert saucer.position.x > u.CENTER.x
        assert saucer._speed < 0

    def test_mystery_score(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(saucer := InvadersSaucer())
        shot = PlayerShot()
        fleets.append(shot)
        shot.position = saucer.position
        saucer.interact_with_playershot(shot, fleets)
        shot.interact_with_invaderssaucer(saucer, fleets)
        score = fi.scores[0]
        assert score.score == 100
        explosions = fi.invader_explosions
        assert len(explosions) == 2





