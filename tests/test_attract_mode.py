from pygame import Vector2
import u
from flyer import InvadersFlyer
from invaders.invader_player import InvaderPlayer
from invaders.raycaster import Raycaster, EmptyCastResult
from invaders.sprite import Spritely, Sprite


class Driver(Spritely, InvadersFlyer):
    def interact_with(self, other, fleets):
        other.interact_with_driver(self, fleets)

    def __init__(self):
        self._sprite = Sprite.player()
        self.step = 4
        half_width = self._sprite.width / 2
        self.left = 64 + half_width
        self.right = 960 - half_width
        self.position = Vector2(self.left, u.INVADER_PLAYER_Y)


class TestAttractMode:
    def test_hookup(self):
        assert 2+2 == 4

    def test_raycaster_exists(self):
        Raycaster()

    def test_empty_scan(self):
        caster = Raycaster()
        x = 15
        result = caster.cast(x)
        assert isinstance(result, EmptyCastResult)

    def test_driver(self):
        driver = Driver()
