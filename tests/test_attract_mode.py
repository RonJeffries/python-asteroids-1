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

    shield_locations = ((198, 286), (378, 466), (558, 646), (738, 826))
    open_locations = (range(0, 198), range(287, 378), range(467, 558), range(647, 738), range(827, 1024))

    def is_in_open(self, x):
        return any([x in r for r in self.open_locations])

    def select_values_in_open(self, x_values):
        in_any_open = [x for x in x_values if self.is_in_open(x)]
        return in_any_open

    def nearest(self, x_values):
        possibles = self.select_values_in_open(x_values)
        if not possibles:
            return self.position.x
        best = possibles[0]
        for x in possibles:
            if abs(self.position.x - x) < abs(self.position.x - best):
                best = x
        return best

    def x_distance(self, position_vector):
        return abs(self.position.x - position_vector.x)

    def interact_with(self, other, fleets):
        other.interact_with_driver(self, fleets)

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

    # open_locations = ((0, 197), (287, 377), (467, 557), (647, 737), (827, 1024))
    def test_find_open_xs(self):
        driver = Driver()
        driver.position = (500, u.INVADER_PLAYER_Y)
        x_in = (190, 290, 490, 690, 890)
        x_out = (250, 390, 590, 790)
        x_values = x_in + x_out
        open_values = driver.select_values_in_open(x_values)
        assert len(open_values) == len(x_in)
        assert all([x in x_in for x in open_values])

    def test_find_nearest_open_x(self):
        driver = Driver()
        driver.position = (500, u.INVADER_PLAYER_Y)
        x_in = (190, 290, 490, 690, 890)
        x_out = (250, 390, 590, 790)
        x_values = x_in + x_out
        nearest_invader_x = driver.nearest(x_values)
        assert nearest_invader_x == 490

    def test_no_open(self):
        driver = Driver()
        driver.position = (500, u.INVADER_PLAYER_Y)
        x_out = (250, 390, 590, 790)
        nearest_invader_x = driver.nearest(x_out)
        assert nearest_invader_x == driver.position.x

    def test_no_invaders(self):
        driver = Driver()
        driver.position = (500, u.INVADER_PLAYER_Y)
        no_invaders = []
        nearest_invader_x = driver.nearest(no_invaders)
        assert nearest_invader_x == driver.position.x


