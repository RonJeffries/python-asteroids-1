from pygame import Vector2

import u
from core.fleets import Fleets
from invaders.invader_player import InvaderPlayer
from invaders.invader_score import InvaderScoreKeeper
from invaders.invaderfleet import InvaderFleet
from invaders.invaders_saucer import InvadersSaucer
from invaders.player_shot import PlayerShot
from tests.tools import FI


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

    def test_does_not_run_with_7_invaders(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(invader_fleet := InvaderFleet())
        invader_group = invader_fleet.invader_group
        assert invader_group.invader_count() == 55
        while invader_group.invader_count() > 7:
            invader_group.kill(invader_group.invaders[0])
        assert invader_group.invader_count() == 7
        fleets.append(saucer := InvadersSaucer())
        assert fi.invader_saucers
        saucer.interact_with_invaderfleet(invader_fleet, fleets)
        saucer.update(1.0/60.0, fleets)
        assert not fi.invader_saucers

    def test_does_run_with_8_invaders(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(invader_fleet := InvaderFleet())
        invader_group = invader_fleet.invader_group
        assert invader_group.invader_count() == 55
        while invader_group.invader_count() > 8:
            invader_group.kill(invader_group.invaders[0])
        assert invader_group.invader_count() == 8
        fleets.append(saucer := InvadersSaucer())
        assert fi.invader_saucers
        saucer.interact_with_invaderfleet(invader_fleet, fleets)
        saucer.update(1.0/60.0, fleets)
        assert fi.invader_saucers

    def test_returns_after_dying(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(saucer := InvadersSaucer())
        stop_loop = 10000
        while fi.invader_saucers and stop_loop > 0:
            saucer.update(1/60, fleets)
            stop_loop -= 1
        assert stop_loop > 0
        assert not fi.invader_saucers
        assert fi.time_capsules

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

        def kill_saucer(expecting):
            saucer.interact_with_playershot(shot, fleets)
            score = fi.scores[-1]
            assert score.score == expecting
            player.fire(fleets)
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




