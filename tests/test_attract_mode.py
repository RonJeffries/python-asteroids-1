from flyer import InvadersFlyer
from invaders.player_shot import PlayerShot
from invaders.raycaster import Raycaster, EmptyCastResult
from invaders.sprite import Spritely, Sprite
from pygame import Vector2
import u


class Driver(Spritely, InvadersFlyer):

    def __init__(self):
        self._sprite = Sprite.player()
        self.step = 4
        half_width = self._sprite.width / 2
        self.left = 64 + half_width
        self.right = 960 - half_width
        self.position = Vector2(self.left, u.INVADER_PLAYER_Y)
        self.count = 0

    def interact_with(self, other, fleets):
        other.interact_with_driver(self, fleets)

    shield_locations = ((198, 286), (378, 466), (558, 646), (738, 826))

    def update(self, delta_time, fleets):
        if self._sprite.centerx < (378+286) / 2:
            centerx = self._sprite.centerx + self.step
            self.position = Vector2(centerx, self.position.y)
        self.count = (self.count + 1) % 60
        if not self.count:
            fleets.append(PlayerShot(self._sprite.center))


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
